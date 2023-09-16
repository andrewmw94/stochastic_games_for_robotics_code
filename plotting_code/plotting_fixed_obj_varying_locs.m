%%
%%% plot fixed object varyign location
clc; clear all; close all;

PLOT = 1;
SAVE = 1;
PLOT_SVG = 0;

%%
%%% plot fixed loc varying location

%% This is unlimited version
% fix 8 location, vary objects
model_constr_time = [0.0372, 0.0812, 0.2762, 1.0778, 5.944];

model_check_time = [0.0418, 0.209, 1.161, 9.3382, 60.9332];

total_time = [0.079, 0.2902, 1.4372, 10.416, 66.8774];

xticks = [1, 2, 3, 4, 5];

plot_graph_unlimited(xticks,model_constr_time, model_check_time, ...
    total_time, PLOT_SVG, SAVE, "8 Loc Varying Objects")

%% This is prob version
% fix 8 location, vary objects
model_constr_time = [0.0416, 0.0876,  0.304, 1.2708, 6.944];

model_check_time = [0.0714,  0.3926, 2.4538, 20.6226, 135.9398];

total_time = [0.113, 0.4802, 2.7578, 21.8934, 142.88389];

xticks = [1, 2, 3, 4, 5];

plot_graph_prob(xticks,model_constr_time, model_check_time, ...
    total_time, PLOT_SVG, SAVE, "8 Loc Varying Objects")

%%
%%%% PLotting fucntion
function plot_graph_unlimited(obj_locs, construct_data, synth_data, total_time, ...
    plot_svg, save_plot, title_str)
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
%     xlabel('Locations', 'FontSize', fontsize)
    ylabel('Time (s)', 'FontSize', fontsize)
    legend('Model Construction', 'Model Checking', 'Total Time', ...
        'Location', 'northwest')
    lgd.FontSize = 12;
%     title(title_str)
    if save_plot == 1
        if  plot_svg == 1
            saveas(f,[pwd, '/unlimited_human/fixed_obj_vary_loc_modified.svg'])
        elseif plot_svg == 0
            saveas(f,[pwd, '/unlimited_human/fixed_obj_vary_loc_modified.png'])
        end
    end
end

function plot_graph_prob(obj_locs, construct_data, synth_data, total_time, ...
    plot_svg, save_plot, title_str)
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
%     xlabel('Locations', 'FontSize', fontsize)
    ylabel('Time (s)', 'FontSize', fontsize)
    lgd = legend('Model Construction', 'Model Checking', 'Total Time', ...
        'Location', 'northwest');
%     fontsize(lgd, 14, 'points');
    lgd.FontSize = 12;
%     title(title_str)
    if save_plot == 1
        if  plot_svg == 1
            saveas(f,[pwd, '/prob_human/fixed_obj_vary_loc_modified.svg'])
        elseif plot_svg == 0
            saveas(f,[pwd, '/prob_human/fixed_obj_vary_loc_modified.png'])
        end
    end
end