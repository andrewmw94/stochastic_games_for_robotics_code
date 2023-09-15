%% Human Unlimited Termination Benchmarking results - average of 5 runs 

clc; clear all; close all;

objs = [1, 2, 3, 4, 5];
PLOT = 1;
SAVE = 1;
PLOT_SVG = 0;

%% For 1 object Model 
model_constr_time = [0.012, 0.0148, 0.0186, 0.0238, 0.0372, ...
    0.0446, 0.079, 0.178, 0.3806, 1.6156, 2.984];

model_check_time = [0.0102, 0.0132, 0.023, 0.0366,...
    0.0418, 0.0646, 0.079, 0.3066, 0.778, 4.2324, 7.8628];

total_time = [0.0222 ,0.028, 0.0416, 0.0604, 0.079, 0.1092, 0.158, ...
    0.4846, 1.1586, 5.848, 10.8468];

One_obj_locs = [4, 5, 6, 7, 8, 9, 10, 15, 20, 30, 35];

if PLOT == 1
    plot_graph(One_obj_locs, model_constr_time, model_check_time, ...\
        total_time, PLOT_SVG, SAVE, "1 Obj Varying Locations", 1);
end

%% For 2 object Model

model_constr_time = [0.0204, 0.0328, 0.0608, 0.0812, 0.167, ...
    0.2116, 1.1586, 5.002];


model_check_time = [0.0282, 0.0596, 0.1094, 0.209, ...
    0.364, 0.5506, 4.8742, 24.0348];

total_time = [0.0486, 0.0924, 0.1702, 0.2902, ...
    0.531, 0.7622, 6.0328, 29.0368];

Two_obj_locs = [5, 6, 7, 8, 9, 10, 15, 20];

if PLOT == 1
    plot_graph(Two_obj_locs, model_constr_time, model_check_time, ...
        total_time, PLOT_SVG, SAVE, '2 Obj Varying Locations', 2);
end


%% For 3 object Model

model_constr_time = [0.0654, 0.1618, 0.2762, 0.4964, 0.8842, ...
    1.6704, 3.053, 5.2164, 8.2372];


model_check_time = [0.1674, 0.5154, 1.161, 2.6794, 5.9972, ...
    11.5222, 21.1262, 35.8094, 60.7998];

total_time = [0.2328, 0.6772, 1.4372, 3.1758, 6.8814, ...
    13.1926, 24.1792, 41.0258, 69.037];

Three_obj_locs = [6, 7, 8, 9, 10, 11, 12, 13, 14];

if PLOT == 1
    plot_graph(Three_obj_locs, model_constr_time, model_check_time, ...
        total_time, PLOT_SVG, SAVE, '3 Obj Varying Locations', 3);
end

%% For 4 object Model

model_constr_time = [0.41, 1.0778, 2.8916, 6.6002, 14.5264];

model_check_time = [2.349, 9.3382, 25.4126, 63.529, 141.2056];

total_time = [2.759, 10.416, 28.3042, 70.1292, 155.732];

Four_obj_locs = [7, 8, 9, 10, 11];

if PLOT == 1
    plot_graph(Four_obj_locs, model_constr_time, model_check_time, ...
        total_time, PLOT_SVG, SAVE, '4 Obj Varying Locations', 4);
end

%% For 5 object Model

model_constr_time = [5.944, NaN];


model_check_time = [60.9332, NaN];

total_time = [66.8774, NaN];

Five_obj_locs = [8];

if PLOT == 1
    plot_graph(Five_obj_locs, model_constr_time, model_check_time, ...
        total_time, PLOT_SVG, SAVE, "5 Obj Varying Locations", 5);
end


%%
%%%% PLotting fucntion
function plot_graph(obj_locs, construct_data, synth_data, total_time, ...
    plot_svg, save_plot, title_str, num_of_objs)
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
    legend('Model Construction', 'Model Checking', 'Total Time', ...
        'Location', 'northwest')
    title(title_str)
    if save_plot == 1
        if  plot_svg == 1
            saveas(f,[pwd, sprintf('/unlimited_human/%d_obj_%d_loc.svg', num_of_objs, ...
                length(obj_locs))])
        elseif plot_svg == 0
            saveas(f,[pwd, sprintf('/unlimited_human/%d_obj_%d_loc.png', num_of_objs, ...
                length(obj_locs))])
        end
    end
 
end


