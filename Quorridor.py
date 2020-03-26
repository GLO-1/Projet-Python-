import networkx as nx
import unittest
import copy


def construire_graphe(joueurs, murs_horizontaux, murs_verticaux):
    """
    Crée le graphe des déplacements admissibles pour les joueurs.
    :param joueurs: une liste des positions (x,y) des joueurs.
    :param murs_horizontaux: une liste des positions (x,y) des murs horizontaux.
    :param murs_verticaux: une liste des positions (x,y) des murs verticaux.
    :returns: le graphe bidirectionnel (en networkX) des déplacements admissibles.
    """
    graphe = nx.DiGraph()

    for x in range(1, 10):
        for y in range(1, 10):
            if x > 1:
                graphe.add_edge((x, y), (x-1, y))
            if x < 9:
                graphe.add_edge((x, y), (x+1, y))
            if y > 1:
                graphe.add_edge((x, y), (x, y-1))
            if y < 9:
                graphe.add_edge((x, y), (x, y+1))

    for x, y in murs_horizontaux:
        graphe.remove_edge((x, y-1), (x, y))
        graphe.remove_edge((x, y), (x, y-1))
        graphe.remove_edge((x+1, y-1), (x+1, y))
        graphe.remove_edge((x+1, y), (x+1, y-1))

    for x, y in murs_verticaux:
        graphe.remove_edge((x-1, y), (x, y))
        graphe.remove_edge((x, y), (x-1, y))
        graphe.remove_edge((x-1, y+1), (x, y+1))
        graphe.remove_edge((x, y+1), (x-1, y+1))

    for joueur in map(tuple, joueurs):

        for prédécesseur in list(graphe.predecessors(joueur)):
            graphe.remove_edge(prédécesseur, joueur)

            successeur = (2*joueur[0]-prédécesseur[0],
                          2*joueur[1]-prédécesseur[1])

            if successeur in graphe.successors(joueur) and successeur not in joueurs:
                graphe.add_edge(prédécesseur, successeur)

            else:
                for successeur in list(graphe.successors(joueur)):
                    if prédécesseur != successeur and successeur not in joueurs:
                        graphe.add_edge(prédécesseur, successeur)

    for x in range(1, 10):
        graphe.add_edge((x, 9), 'B1')
        graphe.add_edge((x, 1), 'B2')

    return graphe


class Quoridor:
    def __init__(self, joueurs, murs=None):
        if murs is not None and murs is not dict:
            raise QuoridorError("murs n'est pas un dictionnaire lorsque présent.")
        elif murs is not None:
            for i in murs['horizonraux']:
                if i[0] < 1 or i[0] > 9 or i[1] < 1 or i[1] > 9:
                    raise QuoridorError("la position d'un mur est invalide.")
            for i in murs['verticaux']:
                if i[0] < 1 or i[0] > 9 or i[1] < 1 or i[1] > 9:
                    raise QuoridorError("la position d'un mur est invalide.")
            self.liste_murs = copy.deepcopy(murs)
        elif murs is None:
            self.liste_murs = {'horizontaux': [], 'verticaux': []}
            
