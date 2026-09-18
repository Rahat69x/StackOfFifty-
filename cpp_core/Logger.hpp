#pragma once
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <deque>
#include <mutex>
#include <chrono>
#include <iomanip>
#include <filesystem>
#include "include/nlohmann/json.hpp"

namespace AegisCore {

class Logger {
public:
    static Logger& getInstance() {
        static Logger instance;
        return instance;
    }

    void log(const std::string& level, const std::string& module_name, const std::string& message) {
        std::lock_guard<std::mutex> lock(mutex_);

        auto now = std::chrono::system_clock::now();
        auto in_time_t = std::chrono::system_clock::to_time_t(now);
        std::stringstream ss;
        ss << std::put_time(std::localtime(&in_time_t), "%Y-%m-%d %H:%M:%S");
        std::string timestamp = ss.str();

        // Print to Console
        std::cout << "[" << timestamp << "] [" << level << "] [" << module_name << "] " << message << std::endl;

        // Add to Circular Buffer (max 500 entries)
        nlohmann::json entry = {
            {"timestamp", timestamp},
            {"level", level},
            {"name", module_name},
            {"module", module_name},
            {"message", message}
        };
        log_buffer_.push_back(entry);
        if (log_buffer_.size() > 500) {
            log_buffer_.pop_front();
        }

        // File output
        try {
            if (file_out_.is_open()) {
                file_out_ << "[" << timestamp << "] [" << level << "] [" << module_name << "] " << message << "\n";
                file_out_.flush();
            }
        } catch (...) {}
    }

    void info(const std::string& module_name, const std::string& message) { log("INFO", module_name, message); }
    void warning(const std::string& module_name, const std::string& message) { log("WARNING", module_name, message); }
    void error(const std::string& module_name, const std::string& message) { log("ERROR", module_name, message); }

    nlohmann::json getRecentLogs(size_t limit = 100) {
        std::lock_guard<std::mutex> lock(mutex_);
        nlohmann::json arr = nlohmann::json::array();
        size_t start = log_buffer_.size() > limit ? log_buffer_.size() - limit : 0;
        for (size_t i = start; i < log_buffer_.size(); ++i) {
            arr.push_back(log_buffer_[i]);
        }
        return arr;
    }

private:
    Logger() {
        try {
            std::filesystem::create_directories("logs");
        } catch (...) {}
        file_out_.open("logs/aegiscore_cpp.log", std::ios::app);
    }
    ~Logger() {
        if (file_out_.is_open()) file_out_.close();
    }
    Logger(const Logger&) = delete;
    Logger& operator=(const Logger&) = delete;

    std::mutex mutex_;
    std::deque<nlohmann::json> log_buffer_;
    std::ofstream file_out_;
};

} // namespace AegisCore
