import os
import zipfile
import json
import shutil
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from api.db import get_report_by_id
from api.pdf_generator import create_audit_pdf

router = APIRouter(tags=["Evidence Exporter"])

@router.get("/export/bundle/{report_id}")
async def get_audit_bundle(report_id: str):
    report = get_report_by_id(report_id)
    if not report:
        raise HTTPException(
            status_code=404, 
            detail=f"Query Exception: Audit Record '{report_id}' not discovered in ledger chain."
        )
    
    bundle_workspace = os.path.join("tmp", f"bundle_{report_id}")
    os.makedirs(bundle_workspace, exist_ok=True)
    
    pdf_target_path = os.path.join(bundle_workspace, "audit_report.pdf")
    json_target_path = os.path.join(bundle_workspace, "audit_report.json")
    zip_target_path = os.path.join("tmp", f"{report_id}_compliance_bundle.zip")
    
    try:
        create_audit_pdf(report, pdf_target_path)
        
        with open(json_target_path, "w", encoding="utf-8") as json_file:
            json.dump(report, json_file, indent=2)
            
        with zipfile.ZipFile(zip_target_path, 'w', zipfile.ZIP_DEFLATED) as archive:
            archive.write(pdf_target_path, arcname="audit_report.pdf")
            archive.write(json_target_path, arcname="audit_report.json")
            
        return FileResponse(
            zip_target_path, 
            media_type="application/zip", 
            filename=f"proofscope_bundle_{report_id}.zip"
        )
        
    except Exception as bundle_err:
        raise HTTPException(
            status_code=500, 
            detail=f"Archival Generation Interruption: {str(bundle_err)}"
        )
    finally:
        if os.path.exists(bundle_workspace):
            shutil.rmtree(bundle_workspace)
