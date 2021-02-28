@ECHO OFF
set dir=..\..\implementations
set JAVA_HOME=C:\Program Files\Java\jdk-14.0.2
set ANT_HOME=C:\Users\corny\OneDrive\Uni\7. Semester\BA\role-benchmarks\implementations\apache-ant-1.9.15
IF "%1" == "" (
	set DEG_VER=-deg
) ELSE (
	set DEG_VER=""
)
"%ANT_HOME%"\bin\ant jar -lib %dir%\objectteams\indy-3.8.0\ecotj-head.jar -Dlib=%dir%\objectteams\indy-3.8.0%DEG_VER% -Dsource=14 -Dtarget=14 -Dver=3.8.0 -Dapr=indy -Ddeg=%DEG_VER%
pause