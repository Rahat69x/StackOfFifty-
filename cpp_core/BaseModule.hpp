#pragma once
#include <string>
#include <memory>
#include <vector>
#include "include/nlohmann/json.hpp"
#include "Logger.hpp"
#include "EventBus.hpp"

namespace StackOfFifty {

class BaseModule {
public:
    std::string id;
    std::string name;
    std::string display_name;
    std::string category;
    std::string version = "1.0.0";
    std::string status = "enabled";
    std::string runtime_status = "stopped";
    std::string permission_level = "viewer";
    bool lab_only = false;
    nlohmann::json config;

    BaseModule(const nlohmann::json& mod_config) {
        id = mod_config.value("id", "mod_000");
        name = mod_config.value("name", "unnamed_module");
        display_name = mod_config.value("display_name", "Unnamed Module");
        category = mod_config.value("category", "General");
        version = mod_config.value("version", "1.0.0");
        status = mod_config.value("status", "enabled");
        permission_level = mod_config.value("permission_level", "viewer");
        lab_only = mod_config.value("lab_only", false);
        config = mod_config;
    }

    virtual ~BaseModule() = default;

    // Pure Virtual Lifecycle Methods
    virtual nlohmann::json start() = 0;
    virtual nlohmann::json stop() = 0;
    virtual nlohmann::json status_check() = 0;
    virtual nlohmann::json get_results() = 0;

    virtual nlohmann::json configure(const nlohmann::json& settings) {
        for (auto& [key, val] : settings.items()) {
            config["settings"][key] = val;
        }
        Logger::getInstance().info(name, "Reconfigured module runtime settings.");
        return {{"status", "reconfigured"}, {"module", name}};
    }

    virtual nlohmann::json generate_report() {
        return {
            {"module", display_name},
            {"module_id", id},
            {"category", category},
            {"runtime_status", runtime_status},
            {"status", status_check()},
            {"results", get_results()}
        };
    }

    void emit_event(const std::string& event_type, const nlohmann::json& data) {
        EventBus::getInstance().emit(name, event_type, data);
    }

    nlohmann::json to_summary_json() const {
        return {
            {"id", id},
            {"name", name},
            {"display_name", display_name},
            {"category", category},
            {"version", version},
            {"status", status},
            {"runtime_status", runtime_status},
            {"permission_level", permission_level},
            {"lab_only", lab_only},
            {"is_loaded", true}
        };
    }
};

} // namespace StackOfFifty
