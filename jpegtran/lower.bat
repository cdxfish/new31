FOR /R %%A IN (.) DO cd %%A && (FOR /F %%B IN ('dir /b /l')  DO rename %%B %%B)
 
echo *************************重命名结束*************************
pause