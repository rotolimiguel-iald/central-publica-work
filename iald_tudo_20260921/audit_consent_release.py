import importlib.util
from pathlib import Path
p=Path(__file__).parents[1]/'iald_build18_20260921/audit_mobile_publish.py'
s=importlib.util.spec_from_file_location('audit',p)
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
m.FILES=['android/app/build.gradle','ios/App/App.xcodeproj/project.pbxproj',
 'ios/App/App/public/iald.css','ios/App/App/public/iald.js','ios/App/App/public/index.html',
 'www/iald.css','www/iald.js','www/index.html']
m.main()
