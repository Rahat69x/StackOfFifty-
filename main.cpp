/**
 * StackOfFifty — Modular Cybersecurity Defense & Operations Platform
 * Native C++20 Platform Server Entry Point
 */
#include <iostream>
#include <csignal>
#include "cpp_core/Logger.hpp"
#include "cpp_core/ConfigLoader.hpp"
#include "cpp_core/ModuleRegistry.hpp"
#include "cpp_modules/AllModules.hpp"
#include "cpp_api/Server.hpp"

using namespace StackOfFifty;

ApiServer* g_server = nullptr;

void signalHandler(int signum) {
    Logger::getInstance().info("main", "Received shutdown signal (" + std::to_string(signum) + "). Stopping StackOfFifty...");
    if (g_server) {
        g_server->stop();
    }
}

int main(int argc, char* argv[]) {
    std::signal(SIGINT, signalHandler);
    std::signal(SIGTERM, signalHandler);

    std::cout << R"(
================================================================================
          STACKOFFIFTY — NATIVE C++20 CYBERSECURITY DEFENSE PLATFORM
                100% Native Compiled Blue Team & SOC Engine
================================================================================
)" << std::endl;

    auto& logger = Logger::getInstance();
    logger.info("main", "Booting StackOfFifty C++20 Native Engine...");

    // 1. Load Master Configuration
    auto& configLoader = ConfigLoader::getInstance();
    auto master_cfg = configLoader.getConfig();
    logger.info("main", "Loaded platform configuration: " + configLoader.getPlatformInfo().value("display_name", "StackOfFifty"));

    // 2. Register all 50 C++ Defensive Modules
    logger.info("main", "Registering 50 native C++ cybersecurity modules...");
    registerAllModules(master_cfg);
    logger.info("main", "All 50 defensive modules successfully registered into C++ ModuleRegistry.");

    // 3. Start Default Active Starter Modules
    auto& registry = ModuleRegistry::getInstance();
    std::vector<std::string> starter_ids = {"mod_001", "mod_003", "mod_007", "mod_011", "mod_012"};
    for (const auto& id : starter_ids) {
        if (auto* m = registry.getModule(id)) {
            m->start();
        }
    }

    // 4. Start Native C++ REST API Server
    int port = 8000;
    ApiServer server(port);
    g_server = &server;

    std::cout << "\n[+] Native C++ Engine Ready!" << std::endl;
    std::cout << "    - REST API & Health: http://localhost:8000/api/health" << std::endl;
    std::cout << "    - All 50 Modules:    http://localhost:8000/api/modules" << std::endl;
    std::cout << "    - SOC Dashboard:     http://localhost:3000\n" << std::endl;

    server.start();

    // Graceful cleanup
    logger.info("main", "Stopping all active C++ modules...");
    registry.stopAll();
    logger.info("main", "StackOfFifty C++ Platform terminated gracefully.");

    return 0;
}
