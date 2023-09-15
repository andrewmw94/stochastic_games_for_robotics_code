%{
Plot orginal PRISM Model construction vs Modified Model construction
 computation for 

     1. Fixed object varying locs
     2. Fixed Locs varying Objects 
%}

clc; clear all; close all;

PLOT = 1;
SAVE = 1;
PLOT_SVG = 0;

%% For Probabilistic Termination case

% 1. Fixed object varying locs
total_time_ours = [0.2328, 0.6772, 1.4372, 3.1758, 6.8814];
total_time_org = [28.444, 330.455, 2666.782, NaN, NaN];

Three_obj_locs = [6, 7, 8, 9, 10];

if PLOT == 1
    plot_graph_prob(Three_obj_locs, total_time_ours, total_time_org, ...
    PLOT_SVG, SAVE, '3 Obj Varying Locations');
end


% 2. Fixed Locs varying Objects 
% fix 8 location, vary objects
total_time_ours = [0.2328, 0.6772, 1.4372, 3.1758, 6.8814];
total_time_org = [0.883, 48.714, 2666.782, NaN, NaN];


xticks = [1, 2, 3, 4, 5];

if PLOT == 1
    plot_graph_prob(xticks, total_time_ours, total_time_org, ...
    PLOT_SVG, SAVE, '8 Loc Varying Objects');
end





%% For Unlimited case
% TODO: Need to do these experiments 


%% helper functions for plotting
function plot_graph_unlimited(obj_locs, construct_data, plot_svg, ...
    save_plot, title_str)
    line_thick = 2;
    fontsize = 16;

    f = figure();

    plot(obj_locs, construct_data, '-o', 'LineWidth', line_thick);
    hold on;
    plot(obj_locs, synth_data, '-o', 'LineWidth', line_thick);
    hold on;
    plot(obj_locs, total_time, '-o', 'LineWidth', line_thick);
    grid on
    xticks(obj_locs)
    xlabel('Locations', 'FontSize', fontsize)
    ylabel('Time (s)', 'FontSize', fontsize)
    legend('Model Construction -Ours', 'Model Construction - Original', ...
        'Location', 'northeast')
    title(title_str)
    if save_plot == 1
        if  plot_svg == 1
            saveas(f,[pwd, ...
                '/unlimited_human/fixed_obj_vary_loc_w_org_prism.svg'])
        elseif plot_svg == 0
            saveas(f,[pwd, ...
                '/unlimited_human/fixed_obj_vary_loc_w_org_prism.png'])
        end
    end
end


function plot_graph_prob(obj_locs, construct_data_our, ...
    construct_data_org, plot_svg, save_plot, title_str)
    line_thick = 2;
    fontsize = 16;

    f = figure();

    plot(obj_locs, construct_data_our, '-o', 'LineWidth', line_thick);
    hold on
    plot(obj_locs, construct_data_org, '-o', 'LineWidth', line_thick);
    grid on
    xticks(obj_locs)
    xlabel('Locations', 'FontSize', fontsize)
    ylabel('Time (s)', 'FontSize', fontsize)
    legend('Model Construction -Ours', 'Model Construction - Original', ...
        'Location', 'northeast')
    title(title_str)
    if save_plot == 1
        if  plot_svg == 1
            % '/prob_human/fixed_obj_vary_loc_w_org_prism.svg'
            saveas(f,[pwd, ...
                 '/prob_human/fixed_loc_vary_obj_w_org_prism.svg'
                ])
        elseif plot_svg == 0
            % '/prob_human/fixed_obj_vary_loc_w_org_prism.png'
            saveas(f,[pwd, ...
                '/prob_human/fixed_loc_vary_obj_w_org_prism.svg'])
        end
    end
end