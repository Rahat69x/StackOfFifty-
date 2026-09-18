#pragma once
#include <unordered_map>
#include <memory>
#include <string>
#include <vector>
#include "BaseModule.hpp"
#include "Logger.hpp"

namespace StackOfFifty {

class ModuleRegistry {
public:
    static ModuleRegistry& getInstance() {
        static ModuleRegistry instance;
        return instance;
    }

    void registerModule(std::unique_ptr<BaseModule> module) {
        if (!module) return;
        std::string mod_id = module->id;
        std::string display = module->display_name;
        modules_[mod_id] = std::move(module);
        Logger::getInstance().info("module_registry", "Registered C++ module: " + mod_id + " (" + display + ")");
    }

    BaseModule* getModule(const std::string& id) {
        auto it = modules_.find(id);
        if (it != modules_.end()) {
            return it->second.get();
        }
        return nullptr;
    }

    nlohmann::json listAll() {
        nlohmann::json arr = nlohmann::json::array();
        for (const auto& [id, mod] : modules_) {
            arr.push_back(mod->to_summary_json());
        }
        return arr;
    }

    size_t countLoaded() const {
        return modules_.size();
    }

    nlohmann::json startAll() {
        nlohmann::json res = nlohmann::json::array();
        for (auto& [id, mod] : modules_) {
            res.push_back(mod->start());
        }
        return res;
    }

    void stopAll() {
        for (auto& [id, mod] : modules_) {
            mod->stop();
        }
    }

private:
    ModuleRegistry() = default;
    ModuleRegistry(const ModuleRegistry&) = delete;
    ModuleRegistry& operator=(const ModuleRegistry&) = delete;

    std::unordered_map<std::string, std::unique_ptr<BaseModule>> modules_;
};

} // namespace StackOfFifty
