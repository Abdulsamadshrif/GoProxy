import os
import subprocess
import sys
import datetime
import json
from datetime import datetime

class TestReport:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.passed_tests = []
        self.failed_tests = []
        self.test_details = {}

    def start_execution(self):
        self.start_time = datetime.now()

    def end_execution(self):
        self.end_time = datetime.now()

    def add_test_result(self, test_file, status, error=None, failed_step=None):
        test_info = {
            'file': test_file,
            'status': status,
            'error': error,
            'failed_step': failed_step
        }
        self.test_details[test_file] = test_info
        
        if status == 'PASSED':
            self.passed_tests.append(test_file)
        else:
            self.failed_tests.append(test_file)

    def generate_report(self):
        duration = self.end_time - self.start_time if self.end_time and self.start_time else None
        
        report = f"""
{'='*80}
EXECUTION SUMMARY
{'='*80}
Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S') if self.start_time else 'N/A'}
End Time: {self.end_time.strftime('%Y-%m-%d %H:%M:%S') if self.end_time else 'N/A'}
Total Duration: {str(duration) if duration else 'N/A'}

{'='*80}
TEST RESULTS SUMMARY
{'='*80}
Total Tests: {len(self.test_details)}
Passed Tests: {len(self.passed_tests)}
Failed Tests: {len(self.failed_tests)}

{'='*80}
PASSED TEST CASES
{'='*80}
"""
        for test in self.passed_tests:
            report += f"✓ {test}\n"

        report += f"""
{'='*80}
FAILED TEST CASES
{'='*80}
"""
        for test in self.failed_tests:
            test_info = self.test_details[test]
            report += f"✗ {test}\n"
            if test_info['failed_step']:
                report += f"   Failed Step: {test_info['failed_step']}\n"
            if test_info['error']:
                report += f"   Error: {test_info['error']}\n"
            report += "\n"

        return report

def run_all_tests():
    report = TestReport()
    report.start_execution()
    
    # Get all Python files in the current directory
    python_files = [f for f in os.listdir('.') if f.endswith('.py') and f != 'run_all.py']
    
    for file in python_files:
        print(f"\n{'='*50}")
        print(f"Running {file}")
        print(f"{'='*50}\n")
        
        try:
            # Run each Python file and capture output
            result = subprocess.run(
                [sys.executable, file],
                capture_output=True,
                text=True,
                check=True
            )
            report.add_test_result(file, 'PASSED')
            print(result.stdout)
            
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr if e.stderr else str(e)
            # Try to extract the failed step from the error message
            failed_step = None
            if "Failed Step:" in error_msg:
                failed_step = error_msg.split("Failed Step:")[1].split("\n")[0].strip()
            
            report.add_test_result(file, 'FAILED', error_msg, failed_step)
            print(f"Error running {file}:")
            print(error_msg)
            
        except Exception as e:
            report.add_test_result(file, 'FAILED', str(e))
            print(f"Unexpected error running {file}: {e}")

    report.end_execution()
    
    # Generate and save the report
    report_content = report.generate_report()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_file = f'test_report_{timestamp}.txt'
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"\nTest report has been saved to: {report_file}")
    print("\n" + report_content)

if __name__ == "__main__":
    run_all_tests() 