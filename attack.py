import sys
import timeit
import itertools
import functools
import secrets
import random

def main(argv):
    try:
        protocol=argv[0]
        f = open(argv[1],'r')
        graphlist= [[int(num) for num in line.split(' ')] for line in f]
        f.close()
        corUsers=int(argv[2])
        f = open(argv[3],'r')
#        priorfile=[int(num) for num in f]
        priorfile=[]
        for line in f:
            for x in line.split(' '):
                priorfile.append(float(x))
        f.close()
        f = open(argv[4])
        simulationoutput=f.read().splitlines()
        f.close()
        print('\033[4m\033[1m'+'Attack Information'+'\033[0m')
        print('Protocol: '+protocol)
        print('GraphFile:')
        print(graphlist)
        print('Corrupted Users: ',corUsers)
        print('Prior senders list:')
        print(priorfile)
        print('prior len:'+str(len(priorfile)))
        #print('Simulation Output:')
        #print(simulationoutput)

        if protocol=='dc':
            dc_attack(graphlist,corUsers,priorfile,simulationoutput)
        elif protocol=='crowds':
            crowds_attack(graphlist,corUsers,priorfile,simulationoutput)

    except:
        print('Invalid arguments!')
        print('Execution Example:\npython3 attack.py [dc|crowds] <graph-file> <c> <prior-file> <output-file>' )
        print('1. [dc|crowds]   choose one for attack')
        print('2. <graph-file>  provide name of the file containing graph adjacency matrix')
        print('3. <c>           provide number of corrupted users (0 for none)')
        print('4. <prior-file>  provide name of the file containing sender\'s probability distribution (only for non-corrupted users')
        print('5. <output-file> provide output file created bu simulate.py')



def dc_attack(graph,corrupted,priorfile,simulationoutput):
    print('\n\033[1m'+'Starting dc attack...'+'\033[0m')
    usernum = len(graph)
    print('Total users: ',usernum)
    print('Corrupted Users: ',corrupted)
    f = open('output_attack','w')
    f.close()
    #remove corrupted users from graph
    adjnocor=[]
    if corrupted!=0:
        for i in graph[:-corrupted]:
            adjnocor.append(i[:-corrupted])
    else:
        adjnocor=graph

    #splitting graph to 
    comp=[]
    for nd in range(usernum-corrupted):
        if not(any(nd in sublist for sublist in comp)):
            visited, stack = set(), [nd]*1
            while stack:
                vertex = stack.pop()
                if vertex not in visited:
                    visited.add(vertex)
                    d=set()
                    v=0
                    for i in adjnocor[vertex]:
                        if i==1:
                            d.add(v)
                        v=v+1
                    stack.extend(d-visited)
            comp.append(list(visited))
    print('Graph components: ',comp)
    execcnt=0
    for ex in simulationoutput:
        execcnt+=1
        print('\n------------------------')
        print('Attack for simulation ',execcnt)
        sr, cc = ex.split(' -')
        simresult=[int(i) for i in sr.split(' ')]
        #print('Simulation Results: ',simresult)
        corcoin=[]
        l = [x for x in list(elements.split(';') for elements in cc.strip().split("_")) if x!=['']]
        for x in l:
            t=[int(i) for i in x]
            if not t in corcoin: corcoin.append(t)
        #print('Coins from corrupted users: ',corcoin)
        
        #remove corrupted users from graph
        #adjnocor=[]
        #if corrupted!=0:
        #    for i in graph[:-corrupted]:
        #        adjnocor.append(i[:-corrupted])
        #else:
        #    adjnocor=graph
        #for j in adjnocor:
         #   print(j)

        #splitting graph to 
        #comp=[]
        #for nd in range(usernum-corrupted):
        #    if not(any(nd in sublist for sublist in comp)):
        #        visited, stack = set(), [nd]*1
        #        while stack:
        #            vertex = stack.pop()
        #            if vertex not in visited:
        #                visited.add(vertex)
        #                d=set()
        #                v=0
        #                for i in adjnocor[vertex]:
        #                    if i==1:
        #                        d.add(v)
        #                    v=v+1
        #                stack.extend(d-visited)
        #        comp.append(list(visited))
        #print('Graph components: ',comp)
            
        for i in range(usernum):
            for cr in corcoin:
                if cr[0]==i or cr[1]==i:
                    simresult[i]=simresult[i]^cr[2]
#        print('simresult after cor del:',simresult)
        
        decision=''
        for x in comp:
            s=0
            for i in x:
                s=s+simresult[i]
            if s%2!=0:
                print('Sender is part of component: ',x)
                if len(x)==1:
                    print('Sender is :',x[0])
                    decision=x[0]
                else:
                    maxprior=0
                    sender=[]
                    for j in x:
                        if priorfile[j]>maxprior:
                            sender.clear()
                            sender.append(j)
                            maxprior=priorfile[j]
                        elif priorfile[j]==maxprior:
                            sender.append(j)
                    if len(sender)==1:
                        print('Sender is (from prior):',sender[0])
                        decision=sender[0]
                    else:
                        decision=secrets.choice(sender)
                        print('Sender is (from prior random):',decision)
                        
                break
        
        f = open('output_attack','a')
        f.write(str(decision)+'\n')
        f.close()

        print('------------------------')


def crowds_attack(graph,corrupted,priorfile,simulationoutput):
    print('\n\033[1m'+'Starting crowds attack...'+'\033[0m')
    usernum = len(graph)
    print('Total users: ',usernum)
    print('Corrupted Users: ',corrupted)
    f = open('output_attack','w')
    f.close()

    forward_pos=0.75

    #Finding corrupted users
    cusers=[]
    for cus in range(usernum-1,usernum-int(corrupted)-1,-1):
        cusers.append(cus)

    #splitting graph to
    comp=[]
    for nd in range(usernum):
        if not(any(nd in sublist for sublist in comp)):
            visited, stack = set(), [nd]*1
            while stack:
                vertex = stack.pop()
                if vertex not in visited:
                    visited.add(vertex)
                    d=set()
                    v=0
                    for i in graph[vertex]:
                        if i==1:
                            d.add(v)
                        v=v+1
                    stack.extend(d-visited)
            comp.append(list(visited))
    print('Graph components: ',comp)

    #Calculating Cx,y for not completed graphs in components
    #Using property of completed graphs that every vertex has degree n-1
    notcompletegraphs=[]
    Cxy=[]
    for g in comp:
        iscomplete=True
        for vertex in g:
            s=sum(graph[vertex])
            #print(s)
            #print("len(g) ",len(g))
            if s!=len(g)-1:
                iscomplete=False
                break
        if iscomplete==False:
            iscomplete=True
            #print("Graph is not complete: ",g)
            notcompletegraphs.append(g)
            #print("Calculating Cx,y ...")
            for z in g:
                if z not in cusers:
                    for k in g:
                        if k not in cusers:
                            Cxy.append([z,k,0])
                    Cxy.append([z,'server',0])
            #print(Cxy)
            #input("Press Enter to continue...")
            for vertex in g:
                if vertex not in cusers:
                    #print("Vertex:",vertex)
                    for i in range(0,10000):       
                        forwarding_result=[]
                        forwarding_result.append(vertex)
                        temp_forw=[]
                        temp_forw.append(vertex)
                        for index,val in enumerate(graph[vertex]):
                            if val==1:
                                temp_forw.append(index)
                        forwarding_result.append(secrets.choice(temp_forw))
                        server_waits=True
                        actions=["forwards","delivers"]
                        p=[forward_pos,1-forward_pos]
                        while server_waits:
                            act=random.choices(actions,p)
                            #print("Action: ",act)
                            if act[0]==actions[0]:
                                temp_forw=[]
                                temp_forw.append(forwarding_result[-1])
                                for index,val in enumerate(graph[forwarding_result[-1]]):
                                    if val==1:
                                        temp_forw.append(index)
                                #print("posible ",temp_forw)
                                forwarding_result.append(secrets.choice(temp_forw))
                            elif act[0]==actions[1]:
                                server_waits=False
                        ffftocor=False
                        #print(forwarding_result)
                        for x in range(0,len(forwarding_result)):
                            if forwarding_result[x] in cusers:
                                for l in range(0,len(Cxy)):
                                    if Cxy[l][0]==vertex and Cxy[l][1]==forwarding_result[x-1]:
                                        Cxy[l][2]=Cxy[l][2]+1
                                        ffftocor=True
                                        break
                                break
                        if ffftocor==False:
                            for l in range(0,len(Cxy)):
                                if Cxy[l][0]==vertex and Cxy[l][1]=='server':
                                    Cxy[l][2]=Cxy[l][2]+1
                                    ffftocor=False
                                    break
    print(Cxy)
    for i in range(0,len(Cxy)):
        Cxy[i][2]=Cxy[i][2]/10000
    #print("Cxy probability: ")
    #for z in Cxy:
        #print(z)

    execcnt=0
    for ex in simulationoutput:
        execcnt+=1
        print('\n------------------------')
        print('Attack for simulation ',execcnt)
        
        fc, ds = ex.split('&')
        deliverer, tosrv = ds.split('@')
        deliverer=int(deliverer)
        
        postprob=[]

        if fc is not '':
            firstdetected, cordetect = fc.split('@')
            firstdetected=int(firstdetected)
            print('First detection forwarded to corrupted: ',firstdetected)
            print('Delivered to server: ',deliverer)
 
            #Finding component that message came from
            gcomp=[]
            for x in comp:
                if deliverer in x:
                    print('Message from graph component:',x)
                    gcomp=x
                    break

            if gcomp in notcompletegraphs:
                print("Graph is not complete",gcomp)
                print("Calculating posteriors using Cx,y...")
                #sum prior for normalization
                sumpriors=0
                for u in gcomp:
                    if u not in cusers:
                        #print("suming prior of user:",u)
                        sumpriors=sumpriors+priorfile[u]
                #print("sumprior: ",sumpriors)
                for vertex in gcomp:
                    if vertex in cusers:
                        postprob.append([vertex,0])
                    else:
                        temp=0
                        for zz in Cxy:
                            if zz[0]==vertex and zz[1]==firstdetected:
                                #print("Cxy for "+str(zz[0])+" detected "+str(zz[1])+" is "+str(zz[2]))
                                temp=zz[2]
                                break
                        temp = temp* (priorfile[vertex]/sumpriors)
                        postprob.append([vertex,temp])
                #suming for Denominator for calculating posteriors
                sumden=0
                for i in postprob:
                   sumden=sumden+i[1]
                #Calculating posteriors
                for i in range(0,len(postprob)):
                    postprob[i][1] = postprob[i][1]/sumden
                print(postprob)
                  
            else:
                print("Graph is complete.")
                print("Calculating posteriors ...")
                tC=0
                for u in gcomp:
                    if u in cusers:
                        tC=tC+1
                tM=len(gcomp)
                tN=tM-tC
                #print("corrupted for graph: ",tC)
                #print("All users: ",tM)
                #print("Honest users: ",tN)
                
                #sum prior for normalization
                sumpriors=0
                for u in gcomp:
                    if u not in cusers:
                        #print("suming prior of user:",u)
                        sumpriors=sumpriors+priorfile[u]
                #print("sumprior: ",sumpriors)

                for vertex in gcomp:
                    if vertex in cusers:
                        postprob.append([vertex,0])
                    elif vertex==firstdetected:
                        temp = (tC*(tM-forward_pos*(tN-1)))/(tM*(tM-forward_pos*tN))
                        temp = temp* (priorfile[vertex]/sumpriors)
                        postprob.append([vertex,temp])
                        #print(temp)
                    else:
                        temp = (tC*forward_pos)/(tM*(tM-forward_pos*tN))
                        temp = temp * (priorfile[vertex]/sumpriors)
                        postprob.append([vertex,temp])
                        #print(temp)
                #suming for Denominator for calculating posteriors
                sumden=0
                for i in postprob:
                   sumden=sumden+i[1]
                #Calculating posteriors
                for i in range(0,len(postprob)):
                    postprob[i][1] = postprob[i][1]/sumden
                print(postprob)


        elif fc is '':
            print('Delivered to server: ',deliverer)
            #Finding component that message came from
            gcomp=[]
            for x in comp:
                if deliverer in x:
                    print('Message from graph component:',x)
                    gcomp=x
                    break
            
            #if corrupted but no detect
            tC=0
            for u in gcomp:
                if u in cusers:
                    tC=tC+1
            
            if tC>0:

                if gcomp in notcompletegraphs:
                    print("Graph is not complete",gcomp)
                    print("Calculating posteriors using Cx,y...")
                    #sum prior for normalization
                    sumpriors=0
                    for u in gcomp:
                        if u not in cusers:
                            #print("suming prior of user:",u)
                            sumpriors=sumpriors+priorfile[u]
                    #print("sumprior: ",sumpriors)
                    for vertex in gcomp:
                        if vertex in cusers:
                            postprob.append([vertex,0])
                        else:
                            temp=0
                            for zz in Cxy:
                                if zz[0]==vertex and zz[1]=='server':
                                    #print("Cxy for "+str(zz[0])+" detected "+str(zz[1])+" is "+str(zz[2]))
                                    temp=zz[2]
                                    break
                            temp = temp* (priorfile[vertex]/sumpriors)
                            postprob.append([vertex,temp])
                    #suming for Denominator for calculating posteriors
                    sumden=0
                    for i in postprob:
                        sumden=sumden+i[1]
                    #Calculating posteriors
                    for i in range(0,len(postprob)):
                        postprob[i][1] = postprob[i][1]/sumden
                    print(postprob)
                    
                else:
                    print("Graph is complete.")
                    print("Calculatin posteriors ...")
                    tM = len(gcomp)
                    tN = tM - tC
                    #sum prior for normalization
                    sumpriors=0
                    for u in gcomp:
                        if u not in cusers:
                            #print("suming prior of user:",u)
                            sumpriors=sumpriors+priorfile[u]
                    #print("sumprior: ",sumpriors)
                    for vertex in gcomp:
                        if vertex in cusers:
                            postprob.append([vertex,0])
                        else:
                            temp = (tN-tN*forward_pos)/(tM-tN*forward_pos)
                            temp = temp * (priorfile[vertex]/sumpriors)
                            postprob.append([vertex,temp])
                    #suming for Denominator for calculating posteriors
                    sumden=0
                    for i in postprob:
                       sumden=sumden+i[1]
                    #Calculating posteriors
                    for i in range(0,len(postprob)):
                        postprob[i][1] = postprob[i][1]/sumden
                    print(postprob)
            
            else:
                # 0 corrupted on graph
                print("0 Corrupted users on graph.")
                print("Atacker is server")
                #sum prior for normalization
                sumpriors=0
                for u in gcomp:
                    if u not in cusers:
                        #print("suming prior of user:",u)
                        sumpriors=sumpriors+priorfile[u]
                #print("sumprior: ",sumpriors)
                tM=len(gcomp)
                for vertex in gcomp:
                    if vertex not in cusers:
                        temp= 1/tM
                        temp= temp * (priorfile[vertex]/sumpriors)
                        postprob.append([vertex,temp])
        #Finding max posterior
        decision=''
        sender=[]
        maxpost=0
        for z in postprob:
            if z[1]>maxpost:
                sender.clear()
                sender.append(z[0])
                maxpost=z[1]
            elif z[1]== maxpost:
                sender.append(z[0])
        if len(sender)==1:
            decision=sender[0]
            print('Possible sender: ',decision)
        else:
            decision=secrets.choice(sender)
            print('Possible sender: ',decision)
    
        f = open('output_attack','a')
        f.write(str(decision)+'\n')
        f.close()




if __name__ == "__main__":
    start = timeit.default_timer()
    main(sys.argv[1:])
    stop = timeit.default_timer()
    print('\nExecution Time: ', stop-start,'\n')
