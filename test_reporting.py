"""
Test Reporting Module for Selenium Test Automation
Provides classes and functions for tracking test execution and generating reports.
"""

import os
import time
from datetime import datetime
from contextlib import contextmanager

class TestStep:
    """Represents a single test step with timing and status information."""
    
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.start_time = None
        self.end_time = None
        self.status = "NOT_STARTED"
        self.error_message = None
    
    def start(self):
        """Start timing the test step."""
        self.start_time = time.time()
        self.status = "RUNNING"
    
    def complete(self, success=True, error_message=None):
        """Complete the test step with success/failure status."""
        self.end_time = time.time()
        self.status = "PASSED" if success else "FAILED"
        self.error_message = error_message
    
    def get_duration(self):
        """Get the duration of the test step in seconds."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None

class TestCase:
    """Represents a complete test case with multiple steps."""
    
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.steps = []
        self.start_time = None
        self.end_time = None
        self.status = "NOT_STARTED"
    
    def start(self):
        """Start the test case."""
        self.start_time = time.time()
        self.status = "RUNNING"
    
    def complete(self, success=True):
        """Complete the test case with success/failure status."""
        self.end_time = time.time()
        self.status = "PASSED" if success else "FAILED"
    
    def add_step(self, step):
        """Add a test step to this test case."""
        self.steps.append(step)
    
    def get_duration(self):
        """Get the total duration of the test case in seconds."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None
    
    def get_passed_steps(self):
        """Get the number of passed steps."""
        return sum(1 for step in self.steps if step.status == "PASSED")
    
    def get_failed_steps(self):
        """Get the number of failed steps."""
        return sum(1 for step in self.steps if step.status == "FAILED")

class TestReport:
    """Manages test execution reporting and generates reports."""
    
    def __init__(self, report_dir):
        self.report_dir = report_dir
        self.test_cases = []
        self.start_time = None
        self.end_time = None
    
    def start(self):
        """Start the test report."""
        self.start_time = time.time()
    
    def complete(self):
        """Complete the test report."""
        self.end_time = time.time()
    
    def add_test_case(self, test_case):
        """Add a test case to the report."""
        self.test_cases.append(test_case)
    
    def get_summary(self):
        """Get a summary of all test results."""
        total_tests = len(self.test_cases)
        passed_tests = sum(1 for tc in self.test_cases if tc.status == "PASSED")
        failed_tests = sum(1 for tc in self.test_cases if tc.status == "FAILED")
        
        total_steps = sum(len(tc.steps) for tc in self.test_cases)
        passed_steps = sum(tc.get_passed_steps() for tc in self.test_cases)
        failed_steps = sum(tc.get_failed_steps() for tc in self.test_cases)
        
        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "total_steps": total_steps,
            "passed_steps": passed_steps,
            "failed_steps": failed_steps,
            "duration": self.get_duration()
        }
    
    def get_duration(self):
        """Get the total duration of all tests in seconds."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None
    
    def generate_html_report(self):
        """Generate an HTML report of the test results."""
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Test Execution Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
        .summary {{ background-color: #e8f5e8; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .test-case {{ border: 1px solid #ddd; margin: 10px 0; border-radius: 5px; }}
        .test-case-header {{ background-color: #f9f9f9; padding: 10px; border-bottom: 1px solid #ddd; }}
        .test-step {{ margin: 5px 10px; padding: 5px; border-left: 3px solid #ddd; }}
        .passed {{ border-left-color: #4CAF50; }}
        .failed {{ border-left-color: #f44336; }}
        .running {{ border-left-color: #2196F3; }}
        .not-started {{ border-left-color: #9E9E9E; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Test Execution Report</h1>
        <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
"""
        
        # Add summary
        summary = self.get_summary()
        duration_str = f"{summary['duration']:.2f}" if summary['duration'] is not None else "N/A"
        html_content += f"""
    <div class="summary">
        <h2>Summary</h2>
        <p><strong>Total Tests:</strong> {summary['total_tests']}</p>
        <p><strong>Passed:</strong> {summary['passed_tests']}</p>
        <p><strong>Failed:</strong> {summary['failed_tests']}</p>
        <p><strong>Total Steps:</strong> {summary['total_steps']}</p>
        <p><strong>Passed Steps:</strong> {summary['passed_steps']}</p>
        <p><strong>Failed Steps:</strong> {summary['failed_steps']}</p>
        <p><strong>Duration:</strong> {duration_str} seconds</p>
    </div>
"""
        
        # Add test cases
        for test_case in self.test_cases:
            status_class = test_case.status.lower()
            duration_str = f"{test_case.get_duration():.2f}" if test_case.get_duration() is not None else "N/A"
            html_content += f"""
    <div class="test-case">
        <div class="test-case-header">
            <h3>{test_case.name}</h3>
            <p><strong>Status:</strong> {test_case.status}</p>
            <p><strong>Description:</strong> {test_case.description}</p>
            <p><strong>Duration:</strong> {duration_str} seconds</p>
        </div>
"""
            
            for step in test_case.steps:
                step_class = step.status.lower().replace('_', '-')
                duration_str = f"{step.get_duration():.2f}" if step.get_duration() is not None else "N/A"
                html_content += f"""
        <div class="test-step {step_class}">
            <p><strong>{step.name}</strong> - {step.description}</p>
            <p>Status: {step.status}</p>
            <p>Duration: {duration_str} seconds</p>
"""
                if step.error_message:
                    html_content += f"<p>Error: {step.error_message}</p>"
                html_content += "</div>"
            
            html_content += "</div>"
        
        html_content += """
</body>
</html>
"""
        
        # Write to file
        report_file = os.path.join(self.report_dir, "test_report.html")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return report_file

    def generate_text_report(self, console_output=""):
        """Generate a text report with console output format."""
        report_content = f"""
Test Execution Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{console_output}

============================================================
FINAL TEST SUMMARY
============================================================
"""
        
        # Add test case results
        for test_case in self.test_cases:
            status_icon = "✓" if test_case.status == "PASSED" else "✗" if test_case.status == "FAILED" else "⚠"
            report_content += f"{status_icon} {test_case.name}: {test_case.status}\n"
        
        # Add overall results
        summary = self.get_summary()
        passed_count = summary['passed_tests']
        failed_count = summary['failed_tests']
        skipped_count = 0  # Not currently tracked
        total_count = summary['total_tests']
        
        report_content += f"""
Overall Results:
  Passed: {passed_count}
  Failed: {failed_count}
  Skipped: {skipped_count}
  Total: {total_count}

Test reports saved in: {self.report_dir}
"""
        
        # Write to file
        report_file = os.path.join(self.report_dir, "test_report.txt")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return report_file

def create_test_case(name, description):
    """Create a new test case."""
    return TestCase(name, description)

@contextmanager
def track_step(test_case, step_name, step_description):
    """Context manager for tracking a test step."""
    step = TestStep(step_name, step_description)
    test_case.add_step(step)
    step.start()
    
    try:
        yield step
        step.complete(success=True)
    except Exception as e:
        step.complete(success=False, error_message=str(e))
        raise 