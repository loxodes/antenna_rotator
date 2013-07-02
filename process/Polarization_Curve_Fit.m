% Polization_Curve_Fit.m
% Written by Russell Carroll, rccarroll@alaska.edu
%
% This function finds the best fit values for the polarization curve
% measured for a given antenna.
%
% [Emax,gamma,phi] = Polarization_Curve_Fit( [ Emeasure; theta] );
%
%   OUTPUTS
%   Emax:  Fitted maximum electric field
%   gamma: Ratio of minimum electric field to Emax
%   phi:   Rotation angle of maximum electric field [rad]
%   
%   INPUTS
%   Emeasure: Mearsured response in RMS electric field
%   theta:     Corresponding angle for Emeasure [rad]
%

function Result = Polarization_Curve_Fit(Emeas, theta)


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                   Main Function Script
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%Find initial values for gamma and phi
Emax = max(Emeas);
Emin = 1./max(1./Emeas);
gamma = Emin/Emax;

phi = theta(min(find(Emeas==Emax)));


    %initial function call
    Get_Error;
    Rsq = Rsq; %call here to allow for sharing with other subfunctions
    
    %find optimal Emax
    Find_Emax;
    
    %find optimal phi
    Find_phi;
    
    %find optimal gamma
    Find_gamma;
    
    %Perform another iteration of each
    Find_Emax;
    Find_phi;
    Find_gamma;
    
%return the resulting values
Result = [Emax,gamma,phi];

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%    
    %subfunction for finding the error
    function Get_Error
        
     	w = theta-phi;
        
        %Find R^2 value (to be minimized by changing phi and gamma)
        Rsq = sum((Emeas-Emax*sqrt(cos(w).^2+(gamma*sin(w)).^2)).^2);
        
        %disp(sprintf('R^2: %0.3f    Emax: %0.2f    phi: %0.1f   gamma: %0.3f',Rsq,Emax,phi*180/pi,gamma));
    end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %subfunction for finding optimal Emax
    function Find_Emax
        % set to a small step size
        E_step = Emax/100;
        
        %perform initial gradiant test of Emax
        Emax = Emax+E_step;
        Rold = Rsq;
        Get_Error;
        Rnew = Rsq;

        %find direction of phi increments
        if Rnew < Rold
            E_incr = E_step;
        else
            E_incr = -E_step;
        end

        %increment in negative gradient
        Emax = Emax + E_incr;
        Rold = Rsq;
        Get_Error;
        Rnew = Rsq;

        %loop until minimum found
        while Rnew < Rold
            Emax = Emax + E_incr;
            Rold = Rsq;
            Get_Error;
            Rnew = Rsq;
        end

        %correct for last increment to give minimum R
        Emax = Emax - E_incr;
        Rold = Rsq;
        Get_Error;
        Rnew = Rsq;
    end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %subfunction for finding optimal phi for the given gamma
    function Find_phi
    
        %perform initial gradiant test of phi (1 degree steps for phi)
        phi = phi+pi/180;
        Rold = Rsq;
        Get_Error;
        Rnew = Rsq;

        %find direction of phi increments
        if Rnew < Rold
            phi_incr = pi/180;
        else
            phi_incr = -pi/180;
        end

        %increment in negative gradient
        phi = phi + phi_incr;
        Rold = Rsq;
        Get_Error;
        Rnew = Rsq;

        %loop until minimum found
        while Rnew < Rold
            phi = phi + phi_incr;
            Rold = Rsq;
            Get_Error;
            Rnew = Rsq;   
        end

        %correct for last increment to give minimum R
        phi = phi - phi_incr;
        Rold = Rsq;
        Get_Error;
        Rnew = Rsq;
    end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %subfunction for finding optimal phi for the given gamma
    function Find_gamma
        
        % set the step size to much smaller than gamma
        gamma_step = gamma/100;
        
        %perform initial gradiant test of gamma (1 degree steps for gamma)
        gamma = gamma+gamma_step;
        Rold = Rsq;
        Get_Error;
        Rnew = Rsq;

        %find direction of phi increments
        if Rnew < Rold
            gamma_incr = gamma_step;
        else
            gamma_incr = -gamma_step;
        end

        %increment in negative gradient
        gamma = gamma+gamma_incr;
        Rold = Rsq;
        Get_Error;
        Rnew = Rsq;

        %loop until minimum found
        while Rnew < Rold
            gamma = gamma+gamma_incr;
            Rold = Rsq;
            Get_Error;
            Rnew = Rsq;  
        end

        %correct for last increment to give minimum R
        gamma = gamma-gamma_incr;
        Rold = Rsq;
        Get_Error;
        Rnew = Rsq;
    end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



end




