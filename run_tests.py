# run_tests.py
async def main():
    # Initialize health monitor
    health_monitor = BrainHealthMonitor()
    
    # Run initial health check
    health_report = await health_monitor.run_health_check()
    print("Initial Health Report:", json.dumps(health_report, indent=2))
    
    # Initialize MOP system
    orchestrator = MOPOrchestrator()
    
    # Test system with sample input
    test_input = {
        "content": "This is a test memory about artificial intelligence",
        "timestamp": datetime.now().isoformat(),
        "source": "test"
    }
    
    try:
        # Process through MOP system
        result = await orchestrator.process_input(test_input)
        print("\nMOP Processing Result:", json.dumps(result, indent=2))
        
        # Run final health check
        final_report = await health_monitor.run_health_check()
        print("\nFinal Health Report:", json.dumps(final_report, indent=2))
        
    except Exception as e:
        print(f"Error during test: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())