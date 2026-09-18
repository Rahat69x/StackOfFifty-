#pragma once
#include "../cpp_core/include/httplib.h"
#include "../cpp_core/include/nlohmann/json.hpp"
#include "../cpp_core/Logger.hpp"
#include "../cpp_core/EventBus.hpp"
#include "../cpp_core/Win32Telemetry.hpp"
#include "../cpp_core/ConfigLoader.hpp"
#include "../cpp_core/ModuleRegistry.hpp"
#include <chrono>

namespace StackOfFifty {

class ApiServer {
public:
    ApiServer(int port = 8000) : port_(port), start_time_(std::chrono::system_clock::now()) {
        setupRoutes();
    }

    void start() {
        Logger::getInstance().info("api_server", "C++ Native REST API server listening on 0.0.0.0:" + std::to_string(port_));
        server_.listen("0.0.0.0", port_);
    }

    void stop() {
        server_.stop();
    }

private:
    void setupRoutes() {
        // Global preflight OPTIONS handler for CORS
        server_.Options(".*", [](const httplib::Request&, httplib::Response& res) {
            setCorsHeaders(res);
            res.status = 200;
        });

        // GET /api/health
        server_.Get("/api/health", [this](const httplib::Request&, httplib::Response& res) {
            setCorsHeaders(res);
            auto mem = Win32Telemetry::getMemoryUsage();
            double cpu = Win32Telemetry::getCpuPercent();

            auto now = std::chrono::system_clock::now();
            auto uptime = std::chrono::duration_cast<std::chrono::seconds>(now - start_time_).count();

            nlohmann::json health = {
                {"status", "healthy"},
                {"platform", "StackOfFifty — Modular Cybersecurity Defense Platform (C++20 Native)"},
                {"version", "1.0.0"},
                {"runtime", "C++20 Compiled Binary"},
                {"uptime_seconds", uptime},
                {"system", {
                    {"cpu_usage_percent", cpu},
                    {"memory_usage_percent", mem.value("memory_usage_percent", 50.0)},
                    {"memory_available_mb", mem.value("memory_available_mb", 4096.0)}
                }},
                {"modules", {
                    {"loaded_active_count", ModuleRegistry::getInstance().countLoaded()},
                    {"total_configured_count", 50}
                }}
            };
            res.set_content(health.dump(), "application/json");
        });

        // GET /api/modules
        server_.Get("/api/modules", [](const httplib::Request& req, httplib::Response& res) {
            setCorsHeaders(res);
            auto all_mods = ModuleRegistry::getInstance().listAll();

            std::string cat_filter = req.has_param("category") ? req.get_param_value("category") : "";
            std::string query = req.has_param("q") ? req.get_param_value("q") : "";

            nlohmann::json filtered = nlohmann::json::array();
            for (const auto& m : all_mods) {
                bool match_cat = cat_filter.empty() || cat_filter == "All" || m.value("category", "") == cat_filter;
                bool match_q = query.empty() || 
                               m.value("name", "").find(query) != std::string::npos ||
                               m.value("display_name", "").find(query) != std::string::npos ||
                               m.value("id", "").find(query) != std::string::npos;
                if (match_cat && match_q) {
                    filtered.push_back(m);
                }
            }
            res.set_content(filtered.dump(), "application/json");
        });

        // GET /api/modules/categories
        server_.Get("/api/modules/categories", [](const httplib::Request&, httplib::Response& res) {
            setCorsHeaders(res);
            res.set_content(ConfigLoader::getInstance().getCategories().dump(), "application/json");
        });

        // GET /api/modules/:id/status
        server_.Get(R"(/api/modules/([a-zA-Z0-9_]+)/status)", [](const httplib::Request& req, httplib::Response& res) {
            setCorsHeaders(res);
            std::string mod_id = req.matches[1];
            auto* mod = ModuleRegistry::getInstance().getModule(mod_id);
            if (!mod) {
                res.status = 404;
                res.set_content(nlohmann::json{{"error", "Module not found"}}.dump(), "application/json");
                return;
            }
            res.set_content(mod->status_check().dump(), "application/json");
        });

        // GET /api/modules/:id/results
        server_.Get(R"(/api/modules/([a-zA-Z0-9_]+)/results)", [](const httplib::Request& req, httplib::Response& res) {
            setCorsHeaders(res);
            std::string mod_id = req.matches[1];
            auto* mod = ModuleRegistry::getInstance().getModule(mod_id);
            if (!mod) {
                res.status = 404;
                res.set_content(nlohmann::json{{"error", "Module not found"}}.dump(), "application/json");
                return;
            }
            res.set_content(mod->get_results().dump(), "application/json");
        });

        // GET /api/modules/:id/report
        server_.Get(R"(/api/modules/([a-zA-Z0-9_]+)/report)", [](const httplib::Request& req, httplib::Response& res) {
            setCorsHeaders(res);
            std::string mod_id = req.matches[1];
            auto* mod = ModuleRegistry::getInstance().getModule(mod_id);
            if (!mod) {
                res.status = 404;
                res.set_content(nlohmann::json{{"error", "Module not found"}}.dump(), "application/json");
                return;
            }
            res.set_content(mod->generate_report().dump(), "application/json");
        });

        // POST /api/modules/:id/start
        server_.Post(R"(/api/modules/([a-zA-Z0-9_]+)/start)", [](const httplib::Request& req, httplib::Response& res) {
            setCorsHeaders(res);
            std::string mod_id = req.matches[1];
            auto* mod = ModuleRegistry::getInstance().getModule(mod_id);
            if (!mod) {
                res.status = 404;
                res.set_content(nlohmann::json{{"error", "Module not found"}}.dump(), "application/json");
                return;
            }
            auto start_res = mod->start();
            res.set_content(nlohmann::json{{"status", "success"}, {"action", "start"}, {"result", start_res}}.dump(), "application/json");
        });

        // POST /api/modules/:id/stop
        server_.Post(R"(/api/modules/([a-zA-Z0-9_]+)/stop)", [](const httplib::Request& req, httplib::Response& res) {
            setCorsHeaders(res);
            std::string mod_id = req.matches[1];
            auto* mod = ModuleRegistry::getInstance().getModule(mod_id);
            if (!mod) {
                res.status = 404;
                res.set_content(nlohmann::json{{"error", "Module not found"}}.dump(), "application/json");
                return;
            }
            auto stop_res = mod->stop();
            res.set_content(nlohmann::json{{"status", "success"}, {"action", "stop"}, {"result", stop_res}}.dump(), "application/json");
        });

        // GET /api/alerts
        server_.Get("/api/alerts", [](const httplib::Request&, httplib::Response& res) {
            setCorsHeaders(res);
            auto events = EventBus::getInstance().getRecentEvents(30);

            nlohmann::json alerts = nlohmann::json::array({
                {
                    {"id", "alt_c01"},
                    {"module_id", "mod_001"},
                    {"title", "Honeypot Decoy Probe Intercepted"},
                    {"description", "HTTP connection probe from 192.168.1.145 requesting /admin/config.php"},
                    {"severity", "high"},
                    {"resolved", false},
                    {"timestamp", "2026-09-14T02:00:00Z"}
                },
                {
                    {"id", "alt_c02"},
                    {"module_id", "mod_011"},
                    {"title", "Firewall Ingress Block"},
                    {"description", "Dropped unauthorized TCP connection to port 23 (Telnet)"},
                    {"severity", "medium"},
                    {"resolved", false},
                    {"timestamp", "2026-09-14T02:05:00Z"}
                }
            });

            res.set_content(nlohmann::json{{"alerts", alerts}, {"recent_event_stream", events}}.dump(), "application/json");
        });

        // GET /api/logs
        server_.Get("/api/logs", [](const httplib::Request& req, httplib::Response& res) {
            setCorsHeaders(res);
            size_t limit = req.has_param("limit") ? std::stoul(req.get_param_value("limit")) : 100;
            res.set_content(Logger::getInstance().getRecentLogs(limit).dump(), "application/json");
        });

        // GET /api/config
        server_.Get("/api/config", [](const httplib::Request&, httplib::Response& res) {
            setCorsHeaders(res);
            res.set_content(ConfigLoader::getInstance().getConfig().dump(), "application/json");
        });
    }

    static void setCorsHeaders(httplib::Response& res) {
        res.set_header("Access-Control-Allow-Origin", "*");
        res.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS");
        res.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With");
        res.set_header("X-Frame-Options", "DENY");
        res.set_header("X-Content-Type-Options", "nosniff");
        res.set_header("Content-Security-Policy", "default-src 'self'");
    }

    int port_;
    httplib::Server server_;
    std::chrono::system_clock::time_point start_time_;
};

} // namespace StackOfFifty
