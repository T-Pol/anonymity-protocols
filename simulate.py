import sys
import timeit
import secrets
import random
import functools



def main(argv):
    try:
        protocol=argv[0]
        f = open(argv[1],'r')
        graphlist= [[int(num) for num in line.split(' ')] for line in f]
        f.close()
        corUsers=argv[2]
        f = open(argv[3],'r')
        userexeclist=[int(num) for num in f]
        f.close()
        print('\033[4m\033[1m'+'Simulation Information'+'\033[0m')
        print('Protocol: '+protocol)
        print('GraphFile:')
        print(graphlist)
        print('Corrupted Users: '+corUsers)
        print('Senders for simulation:')
        print(userexeclist)
        if protocol=='dc':
            dc(graphlist, userexeclist, corUsers)
        elif protocol=='crowds':
            crowds(graphlist, userexeclist, corUsers)

    
    except:
        print('Invalid arguments!')
        print('Execution Example:\npython3 simulate.py [dc|crowds] <graph-file> <c> <users-file>' )
        print('1. [dc|crowds]   choose one for simulation')
        print('2. <graph-file>  provide name of the file containing graph adjacency matrix')
        print('3. <c>           provide number of corrupted users (0 for none)')
        print('4. <users-file>  provide name of the file containing senders id (one execution per line)')



def dc(graph, userexec, corrupted):
    print('\n\033[1m'+'Starting dc simulation...'+'\033[0m')
    usernum = len(graph)
    print('Total users: ',usernum)
    execcalc=0
    f = open('output','w')
    f.close()
    for ex in userexec:
        execcalc +=1
        print('\nExecution '+str(execcalc))
        print('sender_id: '+str(ex))
        coins=[]
        for i in range(0,usernum):
            for j in range(0,usernum):
                if i<j and graph[i][j]==1:
                    coins.append([i,j,secrets.choice([0,1])])
        #print('Coins[x,y,value]:')
        #print(coins)
        #for v in coins:
         #   print(*v,sep=",")
        
        # user coins finder and calculation of result
        userResult = []
        for x in range(0,usernum):
            #print('\n------------------------')
            #print('Calculating for user: ',x)
            userCoins = [0]
            for coin in coins:
                if coin[0]==x or coin[1]==x:
#                    userCoins.append(coin)
                    userCoins.append(coin[2])
            #print('User coins values:')
            #print(userCoins)
            userResult.append([x, functools.reduce(lambda i, j: int(i)^int(j),userCoins)])
            
#           print('------------------------')
            
        if userResult[ex][1]==0:
            userResult[ex][1]=1
        elif userResult[ex][1]==1:
            userResult[ex][1]=0

        print('\nUser Results [user_id, result]: ')
        res=''
        for v in userResult:
            print(*v,sep=",")
            res+=str(v[1])+' '
        f = open('output','a')
        f.write(res+'-')
        res=''
        for cuser in range(usernum-1,usernum-int(corrupted)-1,-1):
            for coin in coins:
                if coin[0]==cuser or coin[1]==cuser:
                    res+=str(coin[0])+';'+str(coin[1])+';'+str(coin[2])+'_'
        f.write(res+'\n')
        f.close()
        print('------------------------')



def crowds(graph, userexec, corrupted):
    print('\033[1m'+'Starting crowds simulation...'+'\033[0m')
    usernum = len(graph)
    print('Total users: ',usernum)
    
    #Posibility of forwarding the message
    forward_pos=0.75  

    f = open('output','w')
    f.close()    

    #Finding corrupted users
    cusers=[]
    for cus in range(usernum-1,usernum-int(corrupted)-1,-1):
        cusers.append(cus)

    execcalc=0
    for ex in userexec:
        execcalc +=1
        print('\nExecution '+str(execcalc))
        print('sender_id: '+str(ex))
       

        #start by adding initiator to result
        forwarding_result=[]
        forwarding_result.append(ex)

        #The initiator must forward the message to some other user
        #We create a list with all possible users to forward
        temp_forw=[]
        temp_forw.append(ex)
        for index,val in enumerate(graph[ex]):
            if val==1:
                temp_forw.append(index)
        #print("possible for forward:",temp_forw)
        #Choosing user to forward
        forwarding_result.append(secrets.choice(temp_forw))
        #print("forwarding result: ",forwarding_result)

        #After first forward, every user forwards with possibility forward_pos and sends to server with posibility 1-forward_pos 
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
                #print("possible for forward:",temp_forw)
                #Choosing user to forward
                forwarding_result.append(secrets.choice(temp_forw))
                #print("forwarding result: ",forwarding_result)
            elif act[0]==actions[1]:
                print("Message delivered to server after: "+str(len(forwarding_result)-1)+" hops")
                print("Channel created: ",forwarding_result)
                server_waits=False
        resp=''
        if len(cusers)>0:
            for x in range(0,len(forwarding_result)):
                if forwarding_result[x] in cusers:
                    resp=resp+str(forwarding_result[x-1])+"@"+str(forwarding_result[x])
                    break
        
        resp=resp+"&"+str(forwarding_result[-1])+"@server"
        f = open('output','a')
        f.write(resp+"\n")
        f.close()        
        print('------------------------')    


    #End of simulations 

if __name__ == "__main__":   
    start = timeit.default_timer()
    main(sys.argv[1:])
    stop = timeit.default_timer()
    print('\nExecution Time: ', stop-start,'\n')

