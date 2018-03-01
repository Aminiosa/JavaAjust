import math
import os
import subprocess

'''
def chVal(a, b):
        aTemp= math.fabs(a-b)
        As=a+aTemp
        Bs=a-aTemp
    return(As, Bs)'''

def test(a, b):
    cmd = "cd ~/Downloads/Telegram\ Desktop/TestMetrics/src && java -classpath . testProgramm -Xns%(xns)sm -Xms%(xms)sm -Xmx%(xms)sm "  % {"xns": a, "xms": b}
    print(cmd)
    out = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    out = out.stdout.read()
    print(out.decode('utf-8'))
    return(out.decode('utf-8'))

def test1(a, b, mintime):
    pars = ['-XX:NeverTenure', '-XX:+UseSerialGC', '-XX:+UseParallelGC', '-XX:+UseParallelOldGC', '-XX:+UseParNewGC', '-XX:+UseG1GC' ]
    cmd = ''
    appendix = ""
    for i in pars:

        cmd = "cd ~/Downloads/Telegram\ Desktop/TestMetrics/src && java -classpath . testProgramm -Xns%(xns)sm -Xms%(xms)sm -Xmx%(xms)sm %(app)s %(par)s" % {
            "xns": a, "xms": b, "app": appendix, "par": i}
        print(cmd)
        out = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        out = out.stdout.read()
        out = out.decode('utf-8')
        print(out)
        print( "meanings: mintime ", int(mintime), "\t current", int(out))
        if (int(mintime) > int(out)):
            appendix = appendix + " " + i
            rescmd = cmd
            print("cmd is changed to:", cmd, "rescmd:", rescmd)
            mintime = out
    return(mintime, rescmd)



tA=10
tB=512

startM = test(tA, tB)
print("Spented time:", startM)
bestTry=startM
coeff=10
A = test(tA/coeff, tB/coeff)
B = test(tA*coeff, tB*coeff)
counter = 3
accur = 20

while ((math.fabs(int(startM)-int(A))) > int(accur)) or ((math.fabs(int(startM)-int(B))) > int(accur)):
    counter = counter + 1
    if (A < B):
        startM=A
        tA = tA / coeff
        tB = tB / coeff
        A = test(tA - tA/coeff, tB - tB/coeff)
        B = test(tA + tA/coeff, tB + tB/coeff)
    else:
        startM = B
        tA = tA * coeff
        tB = tB * coeff
        A=test(tA - tA/coeff, tB - tB/coeff)
        B=test(tA + tA/coeff, tB + tB/coeff)

print("Result is", startM, "pars:", tA, tB, "at steps:", counter)
mintime, command = test1(tA, tB, startM)
print("best result is", mintime, "with command:\n", command)


