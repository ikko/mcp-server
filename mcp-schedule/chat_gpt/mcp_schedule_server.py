import os
import re
import shlex
import subprocess
from typing import List, Literal, Optional

from crontab import CronTab
from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from rich.console import Console
from rich.table import Table
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse
import typer

console = Console()
app = FastAPI()
cli = typer.Typer()

# ---------------------- Settings ----------------------
class MCPSettings(BaseSettings):
    mcp_only: bool = Field(default=True, alias="MCP_ONLY")
    transport: Literal['stdio', 'sse'] = Field(default='stdio')
    model_config = SettingsConfigDict(env_file=".env")

settings = MCPSettings()

# ---------------------- Models ----------------------
class ScheduleInput(BaseModel):
    expression: str
    command: str

class ScheduleEntry(BaseModel):
    schedule: str
    command: str
    mcp_managed: bool = True

    def to_crontab(self) -> str:
        return f"{self.schedule} {self.command}"

    @classmethod
    def from_crontab_line(cls, line: str):
        parts = shlex.split(line)
        if len(parts) < 6:
            raise ValueError("Invalid crontab line")
        schedule = " ".join(parts[:5])
        command = " ".join(parts[5:])
        mcp_managed = "# mcp" in line
        return cls(schedule=schedule, command=command, mcp_managed=mcp_managed)

# ---------------------- Crontab Logic ----------------------
def parse_human_to_cron(expression: str) -> str:
    # placeholder for NLP parsing of human expression to cron
    # in production, integrate with Claude or NLP module here
    if expression.lower() == "every day at 5pm":
        return "0 17 * * *"
    raise ValueError("Unsupported expression: requires NLP module")

def add_schedule(entry: ScheduleEntry):
    cron = CronTab(user=True)
    job = cron.new(command=entry.command, comment='mcp')
    job.setall(entry.schedule)
    cron.write()

def get_schedules() -> List[ScheduleEntry]:
    cron = CronTab(user=True)
    entries = []
    for job in cron:
        if settings.mcp_only and job.comment != 'mcp':
            continue
        entries.append(ScheduleEntry(schedule=str(job.slices), command=job.command, mcp_managed=(job.comment == 'mcp')))
    return entries

# ---------------------- Rich Output ----------------------
def display_schedules(entries: List[ScheduleEntry]):
    table = Table(title="Active Cron Jobs")
    table.add_column("Schedule", style="cyan")
    table.add_column("Command", style="green")
    table.add_column("MCP Managed", style="magenta")

    for e in entries:
        table.add_row(e.schedule, e.command, str(e.mcp_managed))

    console.print(table)

# ---------------------- FastAPI Routes ----------------------
@app.post("/schedule")
async def schedule_job(input: ScheduleInput):
    try:
        if re.match(r"^([\d*/,-]+\s+){4}[\d*/,-]+$", input.expression):
            schedule = input.expression
        else:
            schedule = parse_human_to_cron(input.expression)
        entry = ScheduleEntry(schedule=schedule, command=input.command)
        add_schedule(entry)
        return {"message": "Scheduled", "cron": entry.to_crontab()}
    except Exception as e:
        return {"error": str(e)}

@app.get("/schedules")
async def list_jobs(request: Request):
    entries = get_schedules()
    if settings.transport == 'sse':
        async def event_generator():
            for e in entries:
                yield {
                    "event": "schedule",
                    "data": f"{e.schedule} {e.command} (mcp={e.mcp_managed})"
                }
        return EventSourceResponse(event_generator())
    return StreamingResponse((f"{e.to_crontab()}\n" for e in entries), media_type="text/plain")

# ---------------------- CLI ----------------------
@cli.command()
def list():
    entries = get_schedules()
    display_schedules(entries)

@cli.command()
def add(expression: str, command: str):
    try:
        if re.match(r"^([\d*/,-]+\s+){4}[\d*/,-]+$", expression):
            schedule = expression
        else:
            schedule = parse_human_to_cron(expression)
        entry = ScheduleEntry(schedule=schedule, command=command)
        add_schedule(entry)
        console.print(f"[bold green]Scheduled:[/bold green] {entry.to_crontab()}")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    cli()
