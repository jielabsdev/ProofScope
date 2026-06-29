# Updated post/verify handler tracking lifecycle
def handle_post_verify(data):
    # Perform existing verification logic over the C++ runtime bridge
    verification_result = verify_data(data)
    
    # New integration: append to the hash-chain ledger immediately after validation passes
    if verification_result.is_valid:
        save_report_to_chain(verification_result.report)
    
    return verification_result
