#pragma once
#include <fstream>
#include <sstream>
#include <string>
#include "include/nlohmann/json.hpp"
#include "Logger.hpp"

namespace StackOfFifty {

class ConfigLoader {
public:
    static ConfigLoader& getInstance() {
        static ConfigLoader instance;
        return instance;
    }

    bool load(const std::string& config_path = "platform.config.json") {
        config_path_ = config_path;
        std::ifstream file(config_path);
        if (!file.is_open()) {
            Logger::getInstance().error("config_loader", "Failed to open " + config_path);
            return false;
        }
        try {
            file >> config_;
            Logger::getInstance().info("config_loader", "Loaded configuration from " + config_path);
            return true;
        } catch (const std::exception& e) {
            Logger::getInstance().error("config_loader", std::string("JSON parse error: ") + e.what());
            return false;
        }
    }

    nlohmann::json getConfig() const {
        return config_;
    }

    nlohmann::json getPlatformInfo() const {
        if (config_.contains("platform")) {
            return config_["platform"];
        }
        return {{"name", "StackOfFifty"}, {"version", "1.0.0"}};
    }

    nlohmann::json getCategories() const {
        if (config_.contains("categories")) {
            return config_["categories"];
        }
        return nlohmann::json::array();
    }

    bool updateConfig(const nlohmann::json& new_cfg) {
        config_ = new_cfg;
        std::ofstream file(config_path_);
        if (!file.is_open()) return false;
        file << config_.dump(2);
        return true;
    }

private:
    ConfigLoader() {
        load();
    }
    ConfigLoader(const ConfigLoader&) = delete;
    ConfigLoader& operator=(const ConfigLoader&) = delete;

    std::string config_path_;
    nlohmann::json config_;
};

} // namespace StackOfFifty
