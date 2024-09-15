import asyncio
import random
from io import StringIO

import pandas as pd
from app.db import DB
from app.models.job import Job, JobCreate
from fastapi import APIRouter, BackgroundTasks, HTTPException
from sqlmodel import select

router = APIRouter()


async def process_csv(job_id: str, csv_contents: str, db: DB):
    await asyncio.sleep(random.randint(4, 10))

    try:
        df = pd.read_csv(StringIO(csv_contents))
        meta = {
            "columns": df.columns.tolist(),
            "types": df.dtypes.astype(str).to_dict(),
            "num_rows": len(df),
        }

        job = await db.get(Job, job_id)
        if not job:
            raise HTTPException(
                status_code=500, detail="Job not found, internal server error."
            )

        job.data = df.to_dict(orient="records")
        job.meta = meta
        job.status = "COMPLETED"

        db.add(job)
        await db.commit()
        await db.refresh(job)

    except Exception as e:
        print(f"process_csv: {str(e)}")
        job = await db.get(Job, job_id)
        if not job:
            raise HTTPException(
                status_code=500, detail="Job not found, internal server error."
            )

        job.status = "FAILED"

        raise e


@router.post("/new")
async def create_job(job_create: JobCreate, db: DB, bg_tasks: BackgroundTasks):
    job = Job(status="PROCESSING", data=[], meta={})
    db.add(job)
    await db.commit()
    await db.refresh(job)

    bg_tasks.add_task(process_csv, job.id, job_create.csv_contents, db)

    return {"message": f"Job with ID {job.id} is now being processed."}


@router.get("/", response_model=list[Job])
async def get_jobs(db: DB):
    stmt = select(Job).limit(10)
    result = await db.execute(stmt)
    jobs = result.scalars().all()

    return [Job(id=job.id, status=job.status, meta=job.meta) for job in jobs]


@router.get("/{job_id}", response_model=Job)
async def get_job(job_id: str, db: DB):
    job = await db.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job with ID {job_id} not found.")

    return job
