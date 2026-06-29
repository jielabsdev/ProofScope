cmake_minimum_required(VERSION 3.24)
project(ProofScope LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(PYBIND11_FINDPYTHON ON)

find_package(pybind11 CONFIG REQUIRED)

add_library(proofscope_verifier STATIC
    engine/src/proof_verifier.cpp
)
target_include_directories(proofscope_verifier PUBLIC engine/include)

pybind11_add_module(proofscope_engine bindings/proofscope_module.cpp)
target_link_libraries(proofscope_engine PRIVATE proofscope_verifier)

# Phase D: pybind11 Native Engine Bridge — single-file proof_verifier module
pybind11_add_module(proof_verifier src/verifier.cpp)

# Phase 2: CLI binary for subprocess-isolated verification
add_executable(verifier_cli bin/verifier_cli.cpp)

install(TARGETS proofscope_engine proof_verifier verifier_cli
    LIBRARY DESTINATION .
    RUNTIME DESTINATION .
)
