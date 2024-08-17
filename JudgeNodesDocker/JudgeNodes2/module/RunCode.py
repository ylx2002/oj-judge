def Compile(rid, opt = ['-O2']):# rid:记录编号 opt:编译选项
    import subprocess
    # 编译程序
    CompileResult = subprocess.run(['g++','./submissions/'+str(rid)+'.cpp','-o','./submissions/'+str(rid)]+opt, capture_output=True, text=True)
    # returncode 命令的返回码 0:正常 1:编译错误
    # stdout 命令的标准输出
    # stderr 命令的错误输出
    return CompileResult

def SetMemoryLimit(MemoryLimit): # 空间限制，先假装能限制
    import resource
    soft_limit = MemoryLimit * 1024 * 1024 
    hard_limit = MemoryLimit * 1024 * 1024 
    resource.setrlimit(resource.RLIMIT_AS, (soft_limit, hard_limit))

"""
def GetMemoryUsage(pid):
    try:
        with open(f'/proc/{pid}/status', 'r') as file:
            for line in file:
                if 'VmRSS:' in line:
                    # VmRSS 是当前进程的驻留集大小，即使用的物理内存
                    return int(line.split()[1])  # 单位是 KB
    except FileNotFoundError:
        return 0  # 如果进程已经结束或文件不存在，返回 0
"""
def Run(rid, pid, lang = 'c++'):# rid:记录编号 pid:题目编号
    import subprocess, time
    ProblemPath = r'./data/'+pid+'/'
    SubmitPath=r'./submissions/' + str(rid)
    with open(ProblemPath + 'config', 'r') as file:
        TimeLimit,MemoryLimit,TestCount = [int(i) for i in file.read().split()]
    
    RunResult=[] #  30 AC 40 WA 50 RE 70 TLE 60 MLE 90 UKE 80 CE
    Time = 0
    for i in range(1, TestCount + 1):
        # 运行测试点 i 
        flag = 0 
        try:

            with open(ProblemPath + str(i) + '.in', 'r') as infile, \
                open(SubmitPath + '.out', 'w') as outfile:
               
                # 设置时间限制为 TimeLimit
                # print("!!!")
                start_time = time.time()
                if lang == 'c++':
                    Tmp = subprocess.run([r'./submissions/' + str(rid)], 
                                        stdin=infile, stdout=outfile,
                                        capture_output=False, text=True, timeout=TimeLimit * 2/1000, preexec_fn=SetMemoryLimit(MemoryLimit))
                    flag = Tmp.returncode
                elif lang == 'python':
                    Tmp = subprocess.run(['python', r'./submissions/' + str(rid) + '.py'], 
                                        stdin=infile, stdout=outfile,
                                        capture_output=False, text=True, timeout=TimeLimit * 2/1000, preexec_fn=SetMemoryLimit(MemoryLimit))
                    flag = Tmp.returncode
                end_time = time.time()
                
        except subprocess.TimeoutExpired:
            RunResult.append(70) # TLE 
            Time = TimeLimit * 2
            continue
        except Exception as e:
            RunResult.append(50) # RE
            continue

        Time = max(Time, 1000 * (end_time - start_time))
        # print(Tmp,'\n',end_time-start_time)
            
        if (end_time-start_time)*1000 > TimeLimit:
            RunResult.append(70) # TLE
            continue

        if (flag != 0):
            RunResult.append(50) # RE
            continue
        # 忽略行末空格、换行进行比较
        Tmp = subprocess.run([r'diff', '-b', ProblemPath+str(i) + '.ans', SubmitPath + '.out'], capture_output=True, text=True)
        # print(Tmp)
        if (Tmp.returncode == 0):
            RunResult.append(30)
        else:
            RunResult.append(40)
        
    return {'runtime':int(Time), 'result':RunResult}

# x=run.Compile('R1') # 编译记录号为 R1 的程序
# run.Run('R1','P1') # 运行记录号为 R1，题号为 P1 的程序 