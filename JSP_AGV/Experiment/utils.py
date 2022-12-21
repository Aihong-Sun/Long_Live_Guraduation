from JSP_AGV.RL_Env.action import action_translator

def test_model(Agent,env,times):
    C=[]
    for _ in range(times):
        state, done = env.reset()
        k=0
        while True:
            action = Agent.test_action(state)
            _,_, done = env.step(action)
            k+=1
            if done == True:
                fitness = env.SF.C_max
                C.append(fitness)
                break
        # print(k)
    return C

def dispatching_rule(env,PDR,times):
    C = []
    for _ in range(times):
        state, done = env.reset()
        while True:
            next_state, reward, done = env.step(PDR)
            if done == True:
                fitness = env.SF.C_max
                C.append(fitness)
                break
    return C