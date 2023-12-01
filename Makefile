start_basex_server_windows:
	@start /min cmd /c "C:\Program Files (x86)\BaseX\bin/basexserver.bat"

run_app:
	@python app.py
	
runApi:
	python .\backend\apiFront.py
