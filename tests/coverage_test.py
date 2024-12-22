import coverage 
import pytest 
 
 
def test_coverage(): 
    cov = coverage.Coverage() 
 
    cov.start() 
 
    pytest.main(['-q', 'test.py']) 
 
    cov.stop() 
    cov.save() 
 
    module_name = 'functions' 
    report = cov.report(show_missing=True, include=f'{module_name}*') 
 
    print(f"Общее покрытие {module_name}: {report:.2f}%") 
 
    assert report >= 100, f"Покрытие для {module_name} меньше, чем ожидалось! Текущее покрытие: {report:.2f}%"