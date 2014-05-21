from randomwalk_parameters import *
from randomwalk_analysis import *
import sys
from numpy import *
import scipy as sc
from scipy import stats

def main():

	filename = FILESTUB
	plotfile = PLOTSTUB

	print 'Starting run: '
	if DISTTYPE == 'uniform':
		print 'Uniform distribution.'
	elif DISTTYPE == 'triangular':
		print 'Triangular distribution.'
	elif DISTTYPE == 'gaussian':
		print 'Normal distribution, sigma = ', GAUSSSIG
	elif DISTTYPE == 'von mises':
		print 'Von Mises distribution, kappa = ', VMKAPPA
        else:
		sys.exit('Unrecognized distribution type.')
	print 'Number of runs: ', NUMRUNS
	print 'Number of steps: ', NUMSTEPS

	runs = zeros(shape=(NV,NUMRUNS))
	trail = zeros(shape=(NV,NUMSTEPS+1))
	stats = zeros(shape=(NSTATS,NUMSTEPS+1))
	runs[0,:] = range(NUMRUNS)
	trail[:,0] = runs[:,39]
	stats[STEP,0] = 0
	stats[:,0] = calcstats(runs)

	output(filename, 0, runs)
	if OUTPLOT:
		stepplot(plotfile, 0, runs)
		histplot(plotfile, 0, runs)
		pathplot(plotfile, 0, trail)
		combplot(plotfile, 0, trail, runs)

	template = "{0:4} {1:4} {2:8} {3:15} {4:8} {5:15}"

	for n in range(1, NUMSTEPS+1):
		runs = evolve(runs, GAUSSSIG)
		output(filename, n, runs)
		trail[:,n] = runs[:,39]
		stats[:,n] = calcstats(runs)
		stats[STEP, n] = n
		print template.format('Step', n, 'CHI**2 NOR', stats[PHICHIN,n], 'CHI**2 UNI', stats[PHICHIU,n])
		if OUTPLOT:
			stepplot(plotfile, n, runs)
			histplot(plotfile, n, runs)
			pathplot(plotfile, n, trail)
			combplot(plotfile, n, trail, runs)
			arotplot(plotfile, n, runs)

	outstats(filename, stats)
	print 'Finished!'

def output(filename, n, runs):

	outfile = filename + "%03d.dat" % n
	out = open(outfile, 'w')

	for i in range(NUMRUNS):
		for j in range(NV):
			out.write( str(runs[j,i]) + '   ')
		out.write('\n')

	out.close()

def outstats(filename, stats):

	outfile = filename + "stats.dat"
	out = open(outfile, 'w')

	for i in range(NUMSTEPS):
		for j in range(NSTATS):
			out.write( str(stats[j,i]) + '   ')
		out.write('\n')

	out.close()

def calcstats(runs):
	
	stats = zeros(NSTATS)
	stats[XMEAN] = mean(runs[X,:])
	stats[YMEAN] = mean(runs[Y,:])
	stats[RMEAN] = mean(runs[R,:])
	stats[PHIMEAN] = mean(runs[PHI,:])
	stats[ROTMEAN] = mean(runs[ROTANG,:])
	stats[XSTD] = std(runs[X,:])
	stats[YSTD] = std(runs[Y,:])
	stats[RSTD] = std(runs[R,:])
	stats[PHISTD] = std(runs[PHI,:])
	stats[ROTSTD] = std(runs[ROTANG,:])
	uni_chi2_phi, p_uni_phi, nor_chi2_phi, p_nor_phi = chi_test(runs[PHI,:])
	uni_chi2_rot, p_uni_rot, nor_chi2_rot, p_nor_rot = chi_test(runs[ROTANG,:])
	stats[PHICHIU] = uni_chi2_phi
	stats[PHICHIN] = nor_chi2_phi
	stats[PHIPUNI] = p_uni_phi
	stats[PHIPNOR] = p_nor_phi
	stats[ROTCHIU] = uni_chi2_rot
	stats[ROTCHIN] = nor_chi2_rot
	stats[ROTPUNI] = p_uni_rot
	stats[ROTPNOR] = p_nor_rot

	if (DISTTYPE == 'uniform') and (p_uni_rot < 0.05):
		print 'Warning. Rotation angle dist not consistent with uniform dist.'
		print 'Uniform: chi2', uni_chi2_rot, 'p-val', p_uni_rot
		print 'Normal:  chi2', nor_chi2_rot, 'p-val', p_nor_rot
	elif (DISTTYPE == 'gaussian') and (p_nor_rot < 0.05):
		print 'Warning. Rotation angle dist not consistent with normal dist.'
		print 'Uniform: chi2', uni_chi2_rot, 'p-val', p_uni_rot
		print 'Normal:  chi2', nor_chi2_rot, 'p-val', p_nor_rot
		print 'Mean:', stats[ROTMEAN], 'Standard deviation:', stats[ROTSTD]
	
	return stats

def evolve(runs, gauss_sig):

	if DISTTYPE == 'uniform':
		rot = [2*pi*random.random()-pi for _ in range(NUMRUNS)]
	elif DISTTYPE == 'triangular':
		rot = [random.triangular(-pi, 0, pi) for _ in range(NUMRUNS)]
	elif DISTTYPE == 'gaussian':
		rot = random.normal(0, gauss_sig, NUMRUNS)
	elif DISTTYPE == 'von mises':
		rot = random.vonmises(0, VMKAPPA, NUMRUNS)
        else:
		sys.exit('Unrecognized distribution type.')

	ang = runs[FACING,:] + rot

	runs[X,:] = runs[X,:] + STEPSIZE*cos(ang)
	runs[Y,:] = runs[Y,:] + STEPSIZE*sin(ang)

	runs[R,:] = sqrt(runs[X,:]**2 + runs[Y,:]**2)
	runs[PHI,:] = arctan2(runs[Y,:], runs[X,:])

	runs[FACING,:] = ang
	runs[ROTANG,:] = rot

	return runs

def chi_test(vals):
	
	NBINS = 20

	hist, bin_edges = histogram(vals, bins=NBINS, range=[-pi, pi], normed=True)

	obs  = hist
	bin_centers = bin_edges[0:-1] + 0.5 * (bin_edges[1] - bin_edges[0])

	uni  = ones(NBINS) * 1.0 / (2.0*pi) 
	sig  = std(vals)
	mu   = mean(vals)
	nor  = (1.0 / (sig * sqrt(2.0*pi))) * exp(-(bin_centers-mu)**2 / (2.0*sig**2))

	uni_chi2 = sum((obs - uni)**2 / uni)
	nor_chi2 = sum((obs - nor)**2 / nor)

	stats_obj_uni = stats.chi2(NBINS - 1)
	stats_obj_nor = stats.chi2(NBINS - 3)

	p_uni = 1.0 - stats_obj_uni.cdf(uni_chi2)
	p_nor = 1.0 - stats_obj_nor.cdf(nor_chi2)

	return uni_chi2, p_uni, nor_chi2, p_nor

def chi_decay():

	NSAMPLES = 100
	DISTTYPE = 'gaussian'
	filename = PLOTSTUB

	sig = logspace(-1.5, 0, 100)
	decay_time = zeros(len(sig))
	error = zeros(len(sig))

	for i in range(len(sig)):

		n_vals = zeros(NSAMPLES)

		for j in range(NSAMPLES):

			print 'Sample ', j, 'Sig', sig[i], 
		
			runs = zeros(shape=(NV,NUMRUNS))
			runs[0,:] = range(NUMRUNS)

			n = 0
			uni_chi2 = 1.0
			while uni_chi2 > 0.1:
				runs = evolve(runs, sig[i])
				uni_chi2, p_uni, nor_chi2, p_nor = chi_test(runs[PHI,:])
				n = n + 1

			n_vals[j] = n
			print 'Decay time: ', n

		decay_time[i] = mean(n_vals)
		error[i] = std(n_vals) / sqrt(NSAMPLES)
			
		print "%%%%%%%%%%%%%%%%%%"
		print 'For sig', sig[i], 'mean', decay_time[i], 'err', error[i]
		print "%%%%%%%%%%%%%%%%%%"

	plotfile = filename + "/decay_time.pdf"
	fig = plot.figure(facecolor='white')
    
	ax1 = plot.subplot(111)
	ax1.errorbar(sig, decay_time, yerr=error, fmt='bo', linewidth=2)
        ax1.set_xlabel(r'Width of Gaussian, $\sigma$')
	ax1.set_ylabel('# of steps to $\chi^2 < 0.1$')
	ax1.set_xscale('log')
	ax1.set_yscale('log')

	slope, intercept, r_value, p_value, std_err = stats.linregress(log(sig),log(decay_time))
	A = exp(intercept)
	gam = slope

	x = logspace(log10(sig).min(), log10(sig).max(), 1000)
	y = A*x**(gam)

	ax1.plot(x, y, 'k-', linewidth=2)

	plot.savefig(plotfile, format='pdf')
	
	print 'Plot in', plotfile

	ax1.clear()
	fig.clear()

