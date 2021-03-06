# Plotting options for plot selection dropdown in the order they occur in the raw input
PLOTTING_OPTIONS = [{'label': 'Basic Statistics', 'value': 0},
                    {'label': 'Per base sequence quality', 'value': 1},
                    {'label': 'Per tile sequence quality',
                     'value': 2},
                    {'label': 'Per sequence quality scores', 'value': 3},
                    {'label': 'Per base sequence content',
                     'value': 4},
                    {'label': 'Per sequence GC content',
                     'value': 5},
                    {'label': 'Per base N content', 'value': 6},
                    {'label': 'Sequence Length Distribution',
                     'value': 7},
                    {'label': 'Sequence Duplication Levels',
                     'value': 8},
                    {'label': 'Adapter Content', 'value': 9},
                    {'label': 'Overrepresented sequences', 'value': 10}]


# IDs from plotting_options sorted into groups of plot types for easier processing
table_ids_without_overrep = [0]
table_ids_with_overrep = [0, 10]
boxplot_ids = [1]
tileplot_id = [2]
graph_ids = [3, 4, 5, 6, 7, 8, 9]


subtitle_3 = 'Quality score distribution over all sequences'
subtitle_4 = 'Sequence content across all bases'
subtitle_5 = 'GC distribution over all sequences'
subtitle_6 = 'N content across all bases'
subtitle_7 = 'Distribution of sequence lengths over all sequences'
subtitle_8 = 'Percent of seqs remaining if deduplicated'
subtitle_9 = '% Adapter'

