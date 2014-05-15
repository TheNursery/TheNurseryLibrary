from randomwalk_parameters import *
import matplotlib
import matplotlib.pyplot as plot
from matplotlib import rc
from numpy import *

def plotallsteps(numsteps):

    filename = FILESTUB
    plotfile = PLOTSTUB

    for n in range(numsteps):
        datfile = filename + "%03d.dat" % n
        runs = readfile(datfile)
        stepplot(plotfile, n, runs)


def stepplot(filename, n, runs):

    plotfile = filename + "/plot/plot%03d.pdf" % n
    fig = plot.figure(facecolor='white')
    
    ax1 = plot.subplot(111)
    ax1.plot(runs[X,:],runs[Y,:],'kx',linewidth=2)
    
    plot.savefig(plotfile, format='pdf')

    ax1.clear()
    fig.clear()


def histplot(filename, n, runs):

    plotfile = filename + "/hist/hist%03d.pdf" % n
    fig = plot.figure(facecolor='white')
    
    ax1 = plot.subplot(211)
    n, bins, patches = ax1.hist(runs[R,:], NUMRUNS/10, normed=1, facecolor='green', alpha=0.75)
    ax1.axis([0.0, 100.0, 0.0, 2.0])
    ax1.set_xlabel('Distance Travelled')
    ax1.set_ylabel('Frequency')
    ax2 = plot.subplot(212)
    n, bins, patches = ax2.hist(runs[PHI,:], NUMRUNS/10, normed=1, facecolor='green', alpha=0.75, range=[-pi, pi])
    x = linspace(-pi, pi, 1000)
    sig  = std(runs[PHI,:])
    mu   = mean(runs[PHI,:])
    nor  = (1.0 / (sig * sqrt(2.0*pi))) * exp(-(x-mu)**2 / (2.0*sig**2))
    ax2.plot(x, nor, 'k-', linewidth=2)
    ax2.plot(x, 1.0 / (2.0*pi) + 0.0*x, 'k:', linewidth=2)
    ax2.axis([-pi, pi, 0.0, 0.5])
    ax2.set_xlabel('Angular Position')
    ax2.set_ylabel('Frequency')
    
    plot.savefig(plotfile, format='pdf')

    ax1.clear()
    ax2.clear()
    fig.clear()


def arotplot(filename, n, runs):

    plotfile = filename + "/arot/arot%03d.pdf" % n
    fig = plot.figure(facecolor='white')
    
    NBINS = NUMRUNS / 10

    ax1 = plot.subplot(111)
    n, bins, patches = ax1.hist(runs[ROTANG,:], NBINS, normed=1, facecolor='green', alpha=0.75, range=[-pi, pi])
    x = linspace(-pi, pi, 1000)
    sig  = std(runs[ROTANG,:])
    mu   = mean(runs[ROTANG,:])
    nor  = (1.0 / (sig * sqrt(2.0*pi))) * exp(-(x-mu)**2 / (2.0*sig**2))
    ax1.plot(x, nor, 'k-', linewidth=2)
    ax1.plot(x, 1.0 / (2.0*pi)  + 0.0*x, 'k:', linewidth=2)
    ax1.axis([-pi, pi, 0.0, 2.0])
    ax1.set_xlabel('Rotation Angle')
    ax1.set_ylabel('Frequency')
    
    plot.savefig(plotfile, format='pdf')

    ax1.clear()
    fig.clear()


def pathplot(filename, n, trail):

    plotfile = filename + "/path/path%03d.pdf" % n
    fig = plot.figure(facecolor='white')
    
    ax1 = plot.subplot(111)
    ax1.plot(trail[X,0:n],trail[Y,0:n],'kx-',linewidth=2)
    ax1.axis([-100, 100, -100, 100])

    plot.savefig(plotfile, format='pdf')

    ax1.clear()
    fig.clear()

def combplot(filename, n, trail, runs):

    plotfile = filename + "/comb/comb%03d.pdf" % n
    fig = plot.figure(facecolor='white')
    
    ax1 = plot.subplot(111)
    ax1.plot(runs[X,:],runs[Y,:],'kx',linewidth=2)
    ax1.plot(trail[X,0:n+1],trail[Y,0:n+1],'bo-',linewidth=2)
    ax1.axis([-40, 40, -40, 40])
    
    plot.savefig(plotfile, format='pdf')

    ax1.clear()
    fig.clear()


def readfile(filename):

    fn = open(filename, 'r')
    data = []
    row = []

    lines = fn.readlines()
    for ln in lines:
        wds = ln.split()
        for wd in wds:
            row.append(float(wd))
            data.append(row)
        runs = array(data)
    return runs

    fn.close()
