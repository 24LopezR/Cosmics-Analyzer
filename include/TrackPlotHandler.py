import math
import os
import ROOT as r
import numpy as np

from include.utils import passIDSelection, angle


class TrackPlotHandler:


    def __init__(self, histfilename, cuts_selection):    
        self.filename = histfilename

        self.h_nmuons = {}
        self.h_nmuons_down = {}
        self.h_nmuons_up = {}
        self.h_pt = {}
        self.h_pt_100 = {}
        self.h_eta = {}
        self.h_eta_down = {}
        self.h_eta_up = {}
        self.h_phi = {}
        self.h_dxy = {}
        self.h_dz = {}
        self.h_Nhits = {}
        self.h_NDThits = {}
        self.h_normalizedChi2 = {}
        self.h_charge_pt = {}        
        self.h_cosalpha = {}
        self.h_dPhi = {}
        self.h_dEta = {}
        self.h_eff_pt = {}
        self.h_eff_eta = {}
        self.h_eff_dxy = {}
        self.h_eff_dxy_cutdz = {}
        self.h_eff_dz = {}
        self.h_eff_dz_cutdxy = {}
        self.h_eff_2D = {}
        self.h_dxy_dz_2D = {}

        self.collections = ['dsa', 'dgl']
        for collection in self.collections:
            self.h_nmuons[collection]        = r.TH1F("h_muons_{0}".format(collection),r";N_{#mu};N events",6,0,6) 
            self.h_nmuons_down[collection]   = r.TH1F("h_muons_down_{0}".format(collection),r";N_{#mu}(#phi<0);N events",6,0,6) 
            self.h_nmuons_up[collection]     = r.TH1F("h_muons_up_{0}".format(collection),r";N_{#mu}(#phi>0);N events",6,0,6) 
            self.h_pt[collection]        = r.TH1F("h_pt_{0}".format(collection),r";p_{T} (GeV);N events",100,0,200)
            self.h_pt_100[collection]    = r.TH1F("h_pt_100_{0}".format(collection),r";p_{T} (GeV);N events",100,0,100)
            self.h_eta[collection]       = r.TH1F("h_eta_{0}".format(collection),r";#eta;N events",100,-0.9,0.9)
            self.h_eta_down[collection]  = r.TH1F("h_eta_down_{0}".format(collection),r";#eta;N events",100,-0.9,0.9)
            self.h_eta_up[collection]    = r.TH1F("h_eta_up_{0}".format(collection),r";#eta;N events",100,-0.9,0.9)
            self.h_phi[collection]       = r.TH1F("h_phi_{0}".format(collection),r";#phi;N events",100,-3.2,3.2)
            self.h_dxy[collection]       = r.TH1F("h_dxy_{0}".format(collection),r";|d_{xy}| (cm);N events",100,0,800)
            self.h_dz[collection]        = r.TH1F("h_dz_{0}".format(collection),r";|d_{z}| (cm);N events",100,0,800)
            self.h_Nhits[collection]     = r.TH1F("h_Nhits_{0}".format(collection),r";nValidMuonHits;N events",100,0,50)
            self.h_NDThits[collection]   = r.TH1F("h_NDThits_{0}".format(collection),r";nValidMuonDTHits;N events",100,0,50)
            self.h_normalizedChi2[collection]     = r.TH1F("h_normalizedChi2_{0}".format(collection),r";#chi^{2}/ndof;N events",100,0,5)
            self.h_charge_pt[collection]     = r.TH1F("h_charge_pt_{0}".format(collection),r";Q/p_{T};N events",100,-0.1,0.1)
            self.h_cosalpha[collection]  = r.TH1F("h_cosalpha_{0}".format(collection),r";cos(#alpha);N events",100,-1,1)
            self.h_dPhi[collection]      = r.TH1F("h_dPhi_{0}".format(collection),r";|#Delta#phi|;N events",100,0,3.2)
            self.h_dEta[collection]      = r.TH1F("h_dEta_{0}".format(collection),r";#Delta#eta;N events",100,-2.4,2.4)
            self.h_eff_pt[collection]    = r.TEfficiency("h_eff_pt_{0}".format(collection), "Efficiency cosmic muons;p_{T} (GeV);Efficiency",    90,0,90)
            self.h_eff_eta[collection]   = r.TEfficiency("h_eff_eta_{0}".format(collection),"Efficiency cosmic muons;#eta;Efficiency",100,-1.2,1.2)
            self.h_eff_dxy[collection]   = r.TEfficiency("h_eff_dxy_{0}".format(collection),"Efficiency cosmic muons;|d_{0}| (cm);Efficiency", 9, np.array([0., 2., 5., 10., 20., 30., 40., 50., 60., 70.]))
            self.h_eff_dxy_cutdz[collection]   = r.TEfficiency("h_eff_dxy_cutdz_{0}".format(collection),"Efficiency cosmic muons;|d_{0}| (cm);Efficiency", 9, 
                                                               np.array([0., 2., 5., 10., 20., 30., 40., 50., 60., 70.]))
            self.h_eff_dz[collection]    = r.TEfficiency("h_eff_dz_{0}".format(collection), "Efficiency cosmic muons;|d_{z}| (cm);Efficiency", 6, np.array([0., 8., 20., 40., 60., 90., 140.]))
            self.h_eff_dz_cutdxy[collection]   = r.TEfficiency("h_eff_dz_cutdxy_{0}".format(collection),"Efficiency cosmic muons;|d_{z}| (cm);Efficiency", 6, 
                                                               np.array([0., 8., 20., 40., 60., 90., 140.]))
            self.h_eff_2D[collection]    = r.TEfficiency("h_eff_2D_{0}".format(collection), "Efficiency cosmic muons;|d_{0}| (cm);|d_{z}| (cm);Efficiency",6,
                                                         np.array([0., 2., 5., 10., 30., 50., 70.]), 6,np.array([0., 8., 20., 40., 60., 90., 140.]))
            self.h_dxy_dz_2D[collection] = r.TH2F("h_dxy_dz_2D_{0}".format(collection), "Displacement cosmic muons;|d_{0}| (cm);|d_{z}| (cm);N events",100,0,500,100,0,700) 
        
        ##### Define cuts of the analysis
        self.cuts = {}
        for collection in self.collections:
            self.cuts[collection] = cuts_selection.format(collection)


    def fillVariableHistograms(self, ev, n, collection, cos_alpha=None):        
        self.h_pt[collection].Fill(eval('ev.{0}_pt[n]'.format(collection)))
        self.h_pt_100[collection].Fill(eval('ev.{0}_pt[n]'.format(collection)))
        self.h_eta[collection].Fill(eval('ev.{0}_eta[n]'.format(collection)))
        self.h_phi[collection].Fill(eval('ev.{0}_phi[n]'.format(collection)))
        self.h_dxy[collection].Fill(eval('abs(ev.{0}_dxy[n])'.format(collection)))
        self.h_dz[collection].Fill(eval('abs(ev.{0}_dz[n])'.format(collection)))
        self.h_Nhits[collection].Fill(eval('ev.{0}_nValidMuonHits[n]'.format(collection)))
        self.h_NDThits[collection].Fill(eval('ev.{0}_nValidMuonDTHits[n]'.format(collection)))
        self.h_normalizedChi2[collection].Fill(eval('ev.{0}_normalizedChi2[n]'.format(collection)))
        self.h_charge_pt[collection].Fill(eval('ev.{0}_charge[n]/ev.{0}_pt[n]'.format(collection)))
        self.h_dxy_dz_2D[collection].Fill(eval('abs(ev.{0}_dxy[n])'.format(collection)), eval('abs(ev.{0}_dz[n])'.format(collection)))


    def fillDimuonVariableHistograms(self, ev, n, i, cos_alpha, collection):
        self.h_cosalpha[collection].Fill(cos_alpha)
        self.h_dPhi[collection].Fill(eval('abs(ev.{0}_phi[n]-ev.{0}_phi[i])'.format(collection)))
        self.h_dEta[collection].Fill(eval('ev.{0}_eta[n]-ev.{0}_eta[i]'.format(collection)))
        self.h_eta_down[collection].Fill(eval('ev.{0}_eta[n]'.format(collection)))
        self.h_eta_up[collection].Fill(eval('ev.{0}_eta[i]'.format(collection)))


    def fillEfficiencyHistograms(self, ev, n, collection, hasProbe=False):
        self.h_eff_pt[collection].Fill(hasProbe, eval('ev.{0}_pt[n]'.format(collection)))
        self.h_eff_eta[collection].Fill(hasProbe, eval('ev.{0}_eta[n]'.format(collection)))
        self.h_eff_dxy[collection].Fill(hasProbe, eval('abs(ev.{0}_dxy[n])'.format(collection)))
        if eval('abs(ev.{0}_dz[n])'.format(collection)) < 8: self.h_eff_dxy_cutdz[collection].Fill(hasProbe, eval('abs(ev.{0}_dxy[n])'.format(collection)))
        self.h_eff_dz[collection].Fill(hasProbe, eval('abs(ev.{0}_dz[n])'.format(collection)))
        if eval('abs(ev.{0}_dxy[n])'.format(collection)) < 2: self.h_eff_dz_cutdxy[collection].Fill(hasProbe, eval('abs(ev.{0}_dz[n])'.format(collection)))
        self.h_eff_2D[collection].Fill(hasProbe, eval('abs(ev.{0}_dxy[n])'.format(collection)), eval('abs(ev.{0}_dz[n])'.format(collection)))


    def processEvent(self, ev):
        for collection in self.collections:
            if eval('ev.n{0}'.format(collection)) < 1: continue
            n_up, n_down = 0,0
            for n in range(eval('ev.n{0}'.format(collection))):
                if eval('ev.{0}_phi[n]'.format(collection)) < 0: n_down += 1
                else: n_up += 1 
            for n in range(eval('ev.n{0}'.format(collection))):
                ## Apply cuts
                if np.prod(eval(self.cuts[collection])):
                    ## Fill variable plots
                    self.fillVariableHistograms(ev, n, collection)
                    ## Check if muon passes ID selection
                    passID = passIDSelection(ev, n, collection)
                    cos_alpha_temp = None
                    if passID:
                        hasProbe, cos_alpha_temp, i = self.findProbe(ev, n, collection, eval('ev.n{0}'.format(collection)))
                        ## Fill efficiency plots
                        self.fillEfficiencyHistograms(ev, n, collection, hasProbe)
                        if hasProbe: self.fillDimuonVariableHistograms(ev, n, i, cos_alpha_temp, collection)
                        break
                    
                    self.h_nmuons[collection].Fill(eval('ev.n{0}'.format(collection)))   
                    self.h_nmuons_down[collection].Fill(n_down)
                    self.h_nmuons_up[collection].Fill(n_up)


    '''
    Given one muon (tag), loop through the other muons in the event to find a matching probe.
    '''
    def findProbe(self, ev, n, col, ntotal):
        existsProbe = False
        cos_alpha = None
    
        if 'dsa' in col:
            phi_tag = eval('ev.{0}_phi[n]'.format(col))
            eta_tag = eval('ev.{0}_eta[n]'.format(col))
            theta_tag = 2 * np.arctan(np.exp(-eta_tag)) - np.pi/2
    
            for i in range(ntotal):
                if i == n: continue
                if eval('ev.{0}_nValidMuonDTHits[i]+ev.{0}_nValidMuonDTHits[i]'.format(col)) <= 0: continue
                phi_temp = eval('ev.{0}_phi[i]'.format(col))
                eta_temp = eval('ev.{0}_eta[i]'.format(col))
                theta_temp = 2 * np.arctan(np.exp(-eta_temp)) - np.pi/2
                v_tag = [np.cos(theta_tag)*np.cos(phi_tag), np.cos(theta_tag)*np.sin(phi_tag), np.sin(theta_tag)]
                v_temp = [np.cos(theta_temp)*np.cos(phi_temp), np.cos(theta_temp)*np.sin(phi_temp), np.sin(theta_temp)]
                cos_alpha_temp = angle(v_tag, v_temp)
                cos_alpha = cos_alpha_temp
                if cos_alpha_temp < np.cos(2.1) :
                    existsProbe = True
                    break
    
        if 'dgl' in col:
            phi_tag = eval('ev.{0}_phi[n]'.format(col))
            eta_tag = eval('ev.{0}_eta[n]'.format(col))
            theta_tag = 2 * np.arctan(np.exp(-eta_tag)) - np.pi/2
    
            for i in range(ntotal):
                if i == n: continue
                if eval('ev.{0}_pt[i]'.format(col)) <= 20: continue
                phi_temp = eval('ev.{0}_phi[i]'.format(col))
                eta_temp = eval('ev.{0}_eta[i]'.format(col))
                theta_temp = 2 * np.arctan(np.exp(-eta_temp)) - np.pi/2
                v_tag = [np.cos(theta_tag)*np.cos(phi_tag), np.cos(theta_tag)*np.sin(phi_tag), np.sin(theta_tag)]
                v_temp = [np.cos(theta_temp)*np.cos(phi_temp), np.cos(theta_temp)*np.sin(phi_temp), np.sin(theta_temp)]
                cos_alpha_temp = angle(v_tag, v_temp)
                cos_alpha = cos_alpha_temp
                if cos_alpha < np.cos(2.8):
                    existsProbe = True
                    break
    
        return existsProbe, cos_alpha, i


    def write(self):
        output = r.TFile(self.filename, "RECREATE")
        for attr, value in self.__dict__.items():
            if attr[0] == 'h' and type(value) == dict:
                for key in value.keys():
                    value[key].Write()
        output.Close()
