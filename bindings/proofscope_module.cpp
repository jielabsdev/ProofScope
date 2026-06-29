#include "proofscope/proof_verifier.hpp"

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <cstdint>
#include <string>
#include <vector>

namespace py = pybind11;

namespace {

py::dict to_python_dict(const proofscope::AuditReport& report) {
    py::list constraints;
    for (const auto& item : report.constraints) {
        py::dict record;
        record["id"] = item.id;
        record["layer"] = item.layer;
        record["satisfied"] = item.satisfied;
        record["confidence"] = item.confidence;
        record["message"] = item.message;
        constraints.append(record);
    }

    py::list trace;
    for (const auto& item : report.trace) {
        py::dict record;
        record["operation"] = item.operation;
        record["layer"] = item.layer;
        record["policy"] = item.policy;
        record["detail"] = item.detail;
        trace.append(record);
    }

    py::dict result;
    result["verified"] = report.verified;
    result["status"] = report.status;
    result["proof_digest"] = report.proof_digest;
    result["verification_time_ms"] = report.verification_time_ms;
    result["constraints"] = constraints;
    result["trace"] = trace;
    return result;
}

}  // namespace

PYBIND11_MODULE(proofscope_engine, module) {
    module.doc() = "ProofScope C++ proof verification bridge";

    module.def("verify_proof_bytes", [](py::bytes proof_bytes) {
        const std::string raw = proof_bytes;
        const std::vector<std::uint8_t> bytes(raw.begin(), raw.end());
        return to_python_dict(proofscope::verify_proof_bytes(bytes));
    });
}
