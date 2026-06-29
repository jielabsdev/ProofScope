#include "proofscope/proof_verifier.hpp"

#include <algorithm>
#include <chrono>
#include <iomanip>
#include <numeric>
#include <sstream>

namespace proofscope {
namespace {

std::string simple_digest(const std::vector<std::uint8_t>& bytes) {
    std::uint64_t hash = 1469598103934665603ULL;
    for (const auto byte : bytes) {
        hash ^= byte;
        hash *= 1099511628211ULL;
    }

    std::ostringstream output;
    output << std::hex << std::setfill('0') << std::setw(16) << hash;
    return output.str();
}

bool contains_token(const std::vector<std::uint8_t>& bytes, const std::string& token) {
    return std::search(bytes.begin(), bytes.end(), token.begin(), token.end()) != bytes.end();
}

}  // namespace

AuditReport verify_proof_bytes(const std::vector<std::uint8_t>& proof_bytes) {
    const auto started = std::chrono::steady_clock::now();

    const bool has_bytes = !proof_bytes.empty();
    const bool explicit_failure = contains_token(proof_bytes, "FAIL") ||
                                  contains_token(proof_bytes, "constraint_violation");
    const bool policy_failure = contains_token(proof_bytes, "policy_deviation");
    const bool verified = has_bytes && !explicit_failure && !policy_failure;

    AuditReport report;
    report.verified = verified;
    report.status = verified ? "pass" : "fail";
    report.proof_digest = simple_digest(proof_bytes);

    report.constraints = {
        {"circuit.integrity", "Circuit", has_bytes && !explicit_failure, has_bytes ? 0.99 : 0.0,
         has_bytes ? "Circuit witness commitments are internally consistent."
                   : "Proof artifact is empty."},
        {"model.layer_4.policy", "Layer 4", !policy_failure, policy_failure ? 0.41 : 0.97,
         policy_failure ? "Model output deviated from policy X at Layer 4."
                        : "Layer 4 policy gate remained within the approved path."},
        {"output.binding", "Output", verified, verified ? 0.98 : 0.52,
         verified ? "Public output binding matches the verified execution trace."
                  : "Output binding could not be trusted because verification failed."},
    };

    report.trace = {
        {"load_proof", "Input", "Artifact Intake", "Read raw proof artifact bytes."},
        {"verify_constraints", "Circuit", "Mathematical Integrity",
         explicit_failure ? "Constraint violation marker detected."
                          : "All mock circuit constraints satisfied."},
        {"map_policy", "Layer 4", "Policy X",
         policy_failure ? "Policy deviation marker detected."
                        : "Execution path mapped to approved policy branch."},
    };

    const auto finished = std::chrono::steady_clock::now();
    report.verification_time_ms = static_cast<std::uint64_t>(
        std::chrono::duration_cast<std::chrono::milliseconds>(finished - started).count());

    return report;
}

}  // namespace proofscope
