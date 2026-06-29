#pragma once

#include <cstdint>
#include <string>
#include <vector>

namespace proofscope {

struct ConstraintRecord {
    std::string id;
    std::string layer;
    bool satisfied;
    double confidence;
    std::string message;
};

struct TraceRecord {
    std::string operation;
    std::string layer;
    std::string policy;
    std::string detail;
};

struct AuditReport {
    bool verified;
    std::string status;
    std::string proof_digest;
    std::uint64_t verification_time_ms;
    std::vector<ConstraintRecord> constraints;
    std::vector<TraceRecord> trace;
};

AuditReport verify_proof_bytes(const std::vector<std::uint8_t>& proof_bytes);

}  // namespace proofscope
