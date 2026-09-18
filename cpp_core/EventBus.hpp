#pragma once
#include <string>
#include <vector>
#include <deque>
#include <unordered_map>
#include <functional>
#include <mutex>
#include <chrono>
#include <sstream>
#include <iomanip>
#include "include/nlohmann/json.hpp"

namespace StackOfFifty {

class EventBus {
public:
    using EventHandler = std::function<void(const nlohmann::json&)>;

    static EventBus& getInstance() {
        static EventBus instance;
        return instance;
    }

    void subscribe(const std::string& event_type, EventHandler handler) {
        std::lock_guard<std::mutex> lock(mutex_);
        subscribers_[event_type].push_back(handler);
    }

    void emit(const std::string& sender, const std::string& event_type, const nlohmann::json& data) {
        auto now = std::chrono::system_clock::now();
        auto in_time_t = std::chrono::system_clock::to_time_t(now);
        std::stringstream ss;
        ss << std::put_time(std::localtime(&in_time_t), "%Y-%m-%d %H:%M:%S");

        nlohmann::json payload = {
            {"timestamp", ss.str()},
            {"sender", sender},
            {"event_type", event_type},
            {"data", data}
        };

        std::vector<EventHandler> callbacks;
        {
            std::lock_guard<std::mutex> lock(mutex_);
            event_history_.push_back(payload);
            if (event_history_.size() > 200) {
                event_history_.pop_front();
            }

            if (subscribers_.find(event_type) != subscribers_.end()) {
                callbacks = subscribers_[event_type];
            }
            if (subscribers_.find("*") != subscribers_.end()) {
                for (const auto& cb : subscribers_["*"]) {
                    callbacks.push_back(cb);
                }
            }
        }

        for (const auto& cb : callbacks) {
            try {
                cb(payload);
            } catch (...) {}
        }
    }

    nlohmann::json getRecentEvents(size_t limit = 50) {
        std::lock_guard<std::mutex> lock(mutex_);
        nlohmann::json arr = nlohmann::json::array();
        size_t start = event_history_.size() > limit ? event_history_.size() - limit : 0;
        for (size_t i = start; i < event_history_.size(); ++i) {
            arr.push_back(event_history_[i]);
        }
        return arr;
    }

private:
    EventBus() = default;
    EventBus(const EventBus&) = delete;
    EventBus& operator=(const EventBus&) = delete;

    std::mutex mutex_;
    std::unordered_map<std::string, std::vector<EventHandler>> subscribers_;
    std::deque<nlohmann::json> event_history_;
};

} // namespace StackOfFifty
