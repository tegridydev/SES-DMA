# test.py
import asyncio
import aiohttp
import sqlite3
from datetime import datetime
import json

class BrainHealthMonitor:
    def __init__(self):
        self.health_metrics = {}
        self.status_checklist = {
            "memory_agent": False,
            "evolution_agent": False,
            "supervisor_agent": False,
            "database_connection": False,
            "api_endpoints": False,
            "memory_coherence": False
        }

    async def run_health_check(self):
        """Run comprehensive health check of the brain system"""
        tests = [
            self.check_agent_endpoints(),
            self.check_database_health(),
            self.check_memory_coherence(),
            self.check_system_resources(),
            self.check_agent_communication()
        ]
        results = await asyncio.gather(*tests)
        return self.compile_health_report(results)

    async def check_agent_endpoints(self):
        """Verify all LLM endpoints are responsive"""
        endpoints = {
            "memory": "http://localhost:1234/v1/chat/completions",  # phi-2
            "evolution": "http://localhost:1235/v1/chat/completions",  # mistral
            "supervisor": "http://localhost:1236/v1/chat/completions"  # llama2
        }
        
        results = {}
        async with aiohttp.ClientSession() as session:
            for agent, url in endpoints.items():
                try:
                    async with session.get(url) as response:
                        results[agent] = response.status == 200
                except:
                    results[agent] = False
        
        return {"agent_status": results}

    async def check_memory_coherence(self):
        """Check memory system coherence"""
        conn = sqlite3.connect('memory.sqlite')
        cursor = conn.cursor()
        
        checks = {
            "stm_count": cursor.execute("SELECT COUNT(*) FROM short_term_memory").fetchone()[0],
            "ltm_count": cursor.execute("SELECT COUNT(*) FROM long_term_memory").fetchone()[0],
            "orphaned_memories": cursor.execute("""
                SELECT COUNT(*) FROM memory_connections 
                WHERE target_id NOT IN (SELECT id FROM long_term_memory)
            """).fetchone()[0]
        }
        
        conn.close()
        return {"memory_coherence": checks}

    def compile_health_report(self, results):
        """Compile health check results into a report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "healthy",
            "checks": results,
            "warnings": [],
            "recommendations": []
        }
        
        # Analyze results and add warnings/recommendations
        for check in results:
            if not all(check.values()):
                report["overall_status"] = "degraded"
                report["warnings"].append(f"Failed check: {check}")
        
        return report