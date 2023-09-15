%% Huan Probabilitis Termination Benchmarking results - average of 5 runs 

clc; clear all; close all;

objs = [1, 2, 3, 4, 5];
PLOT = 1;
SAVE = 1;
PLOT_SVG = 0;

%% For 1 object Model 
model_constr_time = [0.0116 , 0.0148 , 0.0202, 0.0234 , 0.0416 , ...
    0.0476 , 0.058, 0.1824, 0.3968 , 1.7468, 3.218 ];

model_check_time = [0.0102 , 0.0244, 0.0308, 0.0514, 0.0714, 0.104, ...
    0.157, 0.6928, 2.0412, 11.1352, 21.3782];

total_time = [0.0218, 0.0392, 0.051, 0.0748, 0.113, 0.1516, 0.215, ...
    0.8752, 2.438, 12.882, 24.5962 ];

One_obj_locs = [4, 5, 6, 7, 8, 9, 10, 15, 20, 30, 35];

if PLOT == 1
    plot_graph(One_obj_locs, model_constr_time, model_check_time, ...\
        total_time, PLOT_SVG, SAVE, "1 Obj Varying Locations", 1);
end

%% For 2 object Model

model_constr_time = [0.0206, 0.0352, 0.0598, 0.0876, 0.166, ...
    0.2062, 1.2298, 5.402];


model_check_time = [0.0362, 0.08, 0.1808, 0.3926, 0.6374, ...
    1.065, 9.974, 46.737];

total_time = [0.0568, 0.1152, 0.2406, 0.4802, 0.8034, ...
    1.2712, 11.2038, 52.139];

Two_obj_locs = [5, 6, 7, 8, 9, 10, 15, 20];

if PLOT == 1
    plot_graph(Two_obj_locs, model_constr_time, model_check_time, ...
        total_time, PLOT_SVG, SAVE, '2 Obj Varying Locations', 2);
end


%% For 3 object Model

model_constr_time = [0.1062, 0.1482, 0.304, 0.5514, ...
    1.025, 1.8628, 3.3992, 5.692];


model_check_time = [0.3298, 1.0016, 2.4538, 5.8852, 12.2054, ...
    23.8222, 43.3596, 75.021];

total_time = [0.4361, 1.1498, 2.7578, 6.4366, 13.2304, ...
    25.685, 46.7588, 80.713];

Three_obj_locs = [6, 7, 8, 9, 10, 11, 12, 13];

if PLOT == 1
    plot_graph(Three_obj_locs, model_constr_time, model_check_time, ...
        total_time, PLOT_SVG, SAVE, '3 Obj Varying Locations', 3);
end

%% For 4 object Model

model_constr_time = [0.4618, 1.2708, 3.2566, 7.4982];


model_check_time = [5.2128, 20.6226, 55.0892, 136.3254];

total_time = [5.6746, 21.8934, 58.3458, 143.8236];

Four_obj_locs = [7, 8, 9, 10];

if PLOT == 1
    plot_graph(Four_obj_locs, model_constr_time, model_check_time, ...
        total_time, PLOT_SVG, SAVE, '4 Obj Varying Locations', 4);
end

%% For 5 object Model

model_constr_time = [6.944, NaN];


model_check_time = [135.9398, NaN];

total_time = [142.88389, NaN];

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
            saveas(f,[pwd, sprintf('/prob_human/%d_obj_%d_loc.svg', num_of_objs, ...
                length(obj_locs))])
        elseif plot_svg == 0
            saveas(f,[pwd, sprintf('/prob_human/%d_obj_%d_loc.png', num_of_objs, ...
                length(obj_locs))])
        end
    end
 
end


