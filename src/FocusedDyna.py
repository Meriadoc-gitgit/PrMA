"""
-------------------

Contient l'algorithme de Focused Dyna

-------------------
"""

from heapq import heappop, heappush
from PrioritizedReplayAgent import PrioritizedReplayAgent
import numpy as np
from mazemdp.toolbox import egreedy

class FocusedDyna(PrioritizedReplayAgent) : 
    def __init__(self, mdp, alpha, delta, epsilon, max_step ,render, episode) :
       super().__init__(mdp, alpha, delta, epsilon, max_step ,render, episode)
       
       #creation du dictionnaire etat:distance_du_debut
       self.stepsFromStart = {self.start : 0}
       
    def fill_memory(self,experience):
        [state,action,next_state,reward] = experience
        priority = self.compute_priority(state,next_state,reward)
        heappush(self.memory, (-priority, experience))
      
    def compute_priority(self,state,next_state,reward):
        if state not in self.mdp.terminal_states:
            max_reward_next_state=np.max(self.q_table[next_state])
        else:
            max_reward_next_state = 0
        return (pow(self.mdp.gamma,self.stepsFromStart[state]))* (reward + self.mdp.gamma*max_reward_next_state)
    
    """================== METTRE À JOUR LE MODÈLE =================="""  
    def update_memory(self) : 
        """
         Mettre à jour le modèle - instructions correspondantes à la deuxième partie de la boucle

        Arguments
        ----------
            algo -- str : nom de l'algorithme choisie 
            state -- int : état courant
            action -- int : action à effectuer
            next_state -- int : état suivant
            reward -- float : récompense accordée
        ----------      
        
        Returns
        ----------      
    """
        (priority, [state, action, next_state, reward]) = heappop(self.memory)
        #print(state)
        self.update_q_value(state,action,next_state,reward, 1)

    

    """==============================================================================================================="""
  
    def handle_step(self, state,action,next_state,reward):
        """
        Effectue la partie propre à Focused Dyna de la gestion d'un pas dans le monde

        Arguments
        ----------
            state -- int : état courant
            action -- int : action à effectuer
            next_state -- int : état suivant
            reward -- float : récompense accordée

        
        Returns
        ----------      
    """
        priority = self.compute_priority(state,next_state, reward)    
        if priority:
            self.update_q_value(state, action, next_state, reward, self.alpha)
            self.nb_backup+=1  
    
        experience = [state,action,next_state,reward]
        self.fill_memory(experience)