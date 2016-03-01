import percolation as P
from .rdflib import NS
a=NS.rdf.type

def percolationSystem():
    triples=[
            (NS.per.CurrentStatus, a, NS.per.SystemStatus)
            ]
def minimumTestOntology(context="minimum_ontology"):
    triples=[
            (NS.po.FacebookSnapshot,NS.rdfs.subClassOf,NS.po.Snapshot),
            (NS.facebook.user,NS.rdfs.range,NS.po.Participant),
            (NS.facebook.ego,NS.rdfs.domain,NS.po.FacebookSnapshot),
            (NS.facebook.userID,NS.rdfs.subPropertyOf,NS.po.userID),
            ]
    P.add(triples,context=context)
def minimumOntology(context="minimum_ontology"):
    triples=rdfsTriples()
    if context=="triples":
        return triples
    P.add(triples,context=context)

def rdfsTriples():
    """Sub Class/Property and range domain assertions"""
    triples=[
            (NS.po.onlineMetaXMLFile, NS.rdfs.subPropertyOf, NS.void.dataDump),
            (NS.po.onlineMetaXMLFile, NS.rdfs.subPropertyOf, NS.void.dataDump),
            (NS.po.FacebookSnapshot,NS.rdfs.subClassOf,NS.po.Snapshot),


            (NS.po.onlineMetaXMLFile, NS.rdfs.subPropertyOf, NS.void.dataDump),
            (NS.po.onlineMetaTTLFile, NS.rdfs.subPropertyOf, NS.void.dataDump),
            (NS.po.MetaXMLFilename,   NS.rdfs.subPropertyOf, NS.void.dataDump),
            (NS.po.MetaTTLFilename,   NS.rdfs.subPropertyOf, NS.void.dataDump),

            (NS.po.onlineInteractionXMLFile,NS.rdfs.subPropertyOf, NS.void.dataDump),
            (NS.po.onlineinteractionTTLFile,NS.rdfs.subPropertyOf, NS.void.dataDump),
            (NS.po.interactionXMLFilename,  NS.rdfs.subPropertyOf, NS.void.dataDump),
            (NS.po.interactionTTLFilename,  NS.rdfs.subPropertyOf, NS.void.dataDump),
            ]
    return triples

def participantRDFSStructure(): # participant
    triples=[
            (NS.po.Participant, NS.rdfs.subClassOf, NS.foaf.Person),
            (NS.gmane.Participant,NS.rdfs.subClassOf,NS.po.Participant),
            (NS.facebook.Participant,NS.rdfs.subClassOf,NS.po.Participant),
            (NS.tw.Participant,NS.rdfs.subClassOf,NS.po.Participant),
            ]
    return triples

def snapshotRDFSStructure():
    triples=[
            (NS.po.InteractionSnapshot, NS.rdfs.subClassOf, NS.po.Snapshot), # fb, part, tw, irc, gmane, cidade
            (NS.po.FriendshipSnapshot, NS.rdfs.subClassOf, NS.po.Snapshot), # fb, part
            (NS.po.ReportSnapshot, NS.rdfs.subClassOf, NS.po.Snapshot), # aa

            (NS.po.FacebookSnapshot, NS.rdfs.subClassOf, NS.po.Snapshot),
            (NS.po.FacebookInteractionSnapshot, NS.rdfs.subClassOf, NS.po.FacebookSnapshot),
            (NS.po.FacebookInteractionSnapshot, NS.rdfs.subClassOf, NS.po.InteractionSnapshot),

            (NS.po.FacebookFriendshipSnapshot, NS.rdfs.subClassOf, NS.po.FacebookSnapshot),
            (NS.po.FacebookFriendshipSnapshot, NS.rdfs.subClassOf, NS.po.FriendshipSnapshot),

            (NS.po.TwitterSnapshot, NS.rdfs.subClassOf, NS.po.InteractionSnapshot),

            (NS.po.GmaneSnapshot, NS.rdfs.subClassOf, NS.po.InteractionSnapshot),

            (NS.po.IRCSnapshot, NS.rdfs.subClassOf, NS.po.InteractionSnapshot),

            (NS.po.AASnapshot, NS.rdfs.subClassOf, NS.po.ReportSnapshot),

            (NS.po.ParticipaSnapshot, NS.rdfs.subClassOf, NS.po.CompleteSnapshot),

            (NS.po.CidadeDemocraticaSnapshot, NS.rdfs.subClassOf, NS.po.InteractionSnapshot),
            ]
    return triples
def idRDFSStructure():
    # User ID somente, na msg a ID eh a URI pois nao diferem em listas/grupos diferentes
    # Mas IDs podem existir para grupos e pessoas, pois se repetem em datasets diferentes
    triples=[
            (NS.gmane.gmaneID, NS.rdfs.subPropertyOf, NS.po.auxID),
            (NS.facebook.groupID, NS.rdfs.subPropertyOf, NS.po.auxID),

            (NS.facebook.ID, NS.rdfs.subPropertyOf,NS.po.ID),
            (NS.po.numericID, NS.rdfs.subPropertyOf,NS.po.ID),
            (NS.po.stringID, NS.rdfs.subPropertyOf,NS.po.ID),
            (NS.po.auxID, NS.rdfs.subPropertyOf,NS.po.ID),

            (NS.facebook.numericID,NS.rdfs.subPropertyOf,NS.facebook.ID),
            (NS.facebook.numericID,NS.rdfs.subPropertyOf,NS.po.numericID),
            (NS.facebook.stringID, NS.rdfs.subPropertyOf,NS.facebook.ID),
            (NS.facebook.stringID, NS.rdfs.subPropertyOf,NS.po.stringID),

            (NS.gmane.stringID,NS.rdfs.subPropertyOf,NS.po.stringID),
            (NS.gmane.email,   NS.rdfs.subPropertyOf,NS.gmane.stringID),

            (NS.tw.stringID,NS.rdfs.subPropertyOf,NS.po.stringID),
            (NS.tw.email,   NS.rdfs.subPropertyOf,NS.tw.stringID),

            ]
    return triples
def fileRDFSStructure():
    triples=[
            (NS.po.interactionXMLFile, NS.rdfs.subPropertyOf,NS.po.defaultXML), # fb
            (NS.po.rdfFile           , NS.rdfs.subPropertyOf,NS.po.defaultXML), # twitter, gmane
            (NS.po.friendshipXMLFile , NS.rdfs.subPropertyOf,NS.po.defaultXML), # fb
            ]
    return triples
def graphRDFStructure():
    triples=[
            (NS.po.MetaNamedGraph, NS.rdfs.subClassOf,NS.po.NamedGraph),
            (NS.po.TranslationNamedGraph, NS.rdfs.subClassOf, NS.po.NamedGraph),

            (NS.po.metaGraph , NS.rdfs.subPropertyOf,NS.po.namedGraph), # fb
            (NS.po.metaGraph , NS.rdfs.range,NS.po.MetaNamedGraph), # fb
            (NS.po.translationGraph , NS.rdfs.subPropertyOf,NS.po.namedGraph), # fb
            (NS.po.translationGraph , NS.rdfs.range,NS.po.TranslationNamedGraph), # fb
            ]
    return triples
def messageRDFSStructure():
    triples=[
            (NS.gmane.Message,NS.rdfs.subClassOf,NS.po.Message),
            (NS.tw.Message,NS.rdfs.subClassOf,NS.po.Message),
            (NS.po.Message,NS.rdfs.subClassOf,NS.po.InteractionInstance),
            ]
def interactionRDFSStructure():
    triples=[
            (NS.facebook.Interaction,NS.rdfs.subClassOf,NS.po.InteractionInstance),
            (NS.gmane.Response,NS.rdfs.subClassOf,NS.po.InteractionInstance),
            (NS.gmane.Retweet,NS.rdfs.subClassOf,NS.po.InteractionInstance),

            (NS.facebook.nInterations, NS.rdfs.subPropertyOf,NS.facebook.nRelations),
            ]
    return triples
def friendshipRDFSStructure():
    triples=[
            (NS.facebook.friendOf,NS.rdfs.subPropertyOf,NS.po.friendOf),
            (NS.participa.friendOf,NS.rdfs.subPropertyOf,NS.po.friendOf),

            (NS.facebook.nFriendships, NS.rdfs.subPropertyOf,NS.facebook.nRelations),
            ]
    return triples
def friendshipOWLStructure():
    triples=[
            (NS.facebook.friendOf,a,NS.owl.SymmetricProperty),
            ]
    return triples
def participantRelationRDFStructure():
    triples=[
            (NS.facebook.nRelations, NS.rdfs.subPropertyOf,NS.po.nRelations),
            ]
    triples+=friendshipRDFSStructure()+interactionRDFSStructure()
    return triples

def anonymizationRDFSStructure():
    triples=[
            (NS.facebook.anonymized, NS.rdfs.subPropertyOf,NS.po.anonymized),
            (NS.facebook.friendshipsAnonymized, NS.rdfs.subPropertyOf,NS.facebook.anonymized),
            (NS.facebook.interactionssAnonymized, NS.rdfs.subPropertyOf,NS.facebook.anonymized),
            ]
    return triples

def todo():

    todo="""type of relation retrievement: 1, 2 or 3

labels equivalence: irc, etc
date equivalence
interaction/relation uris equivalence
textual content equivalence

if text is available"""
    return todo







