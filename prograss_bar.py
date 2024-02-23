import time

def print_progress_bar(iteration=0, total=100, prefix='Progress:', suffix='Complete', length=50, fill='#'):
    '''
    printout the prograss of the status 
    '''
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
    if iteration == total:
        print()
        pass
    pass

def prog_bar_2(iteration, total, prefix='Progress:', suffix='Complete', length=50, fill_str='=', fill_char='Gary say hi', adjust='right'):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    fill_length = len(fill_char)
    fill_count = min(int(iteration / total * fill_length), fill_length)
    fill_str_length = len(fill_str)
    fill_segment_length = fill_str_length / length
    fill_segment_count = int(filled_length * fill_segment_length)
    fill_segment = fill_str[:fill_segment_count]
    
    if adjust == 'right':
        bar = fill_char * (filled_length - fill_segment_count) + fill_segment + '-' * (length - filled_length)
    else:  # Default to left adjustment
        bar = fill_segment + fill_char * (filled_length - fill_segment_count) + '-' * (length - filled_length)
        
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
    if iteration == total:
        print()


# 測試程式
if __name__ == "__main__":
    total_iterations = 100
    # for i in range(total_iterations + 1):
    #     time.sleep(0.1)  # 模擬一些工作
    #     print_progress_bar(i, total_iterations, prefix='Progress:', suffix='Complete', length=50)

    for i in range(total_iterations + 1):
        time.sleep(0.1)  # 模擬一些工作
        prog_bar_2(i, total_iterations, prefix='Progress:', suffix='Complete', length=50, fill_str='Gary say hi', fill_char='>', adjust='left')