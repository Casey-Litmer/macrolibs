import cProfile
import pstats
from io import StringIO
import inspect


def profile_run(command: str, sort_by: str = 'cumtime', lines = None, precision = 6) -> None:
    """
    A custom profiling function similar to cProfile.run() with enhanced formatting options.

    Parameters:
    - command (str): The string of code to execute (must be a valid Python expression).
    - sort_by (str): The metric to sort the profiling results by. Options: 'tottime', 'cumtime', 'ncalls', etc.
    - lines (int): Number of lines of stats to display.
    - precision (int): Number of decimal places to display for timing statistics.
    """
    # Get the caller's frame
    caller_frame = inspect.stack()[1]

    # Extract globals from the caller's frame (where the function is defined)
    caller_globals = caller_frame[0].f_globals

    #Run Command
    profiler = cProfile.Profile()
    profiler.enable()
    exec(command, caller_globals, locals())
    profiler.disable()

    # Capture profiling stats
    result_stream = StringIO()
    stats = pstats.Stats(profiler, stream=result_stream)
    stats.strip_dirs().sort_stats(sort_by)

    #Print all lines if lines is None
    if lines:
        stats.print_stats(lines)
    else:
        stats.print_stats()

    # Customize precision in the output
    formatted_output = result_stream.getvalue()
    # Adjust decimal places by formatting lines with timing data
    lines = formatted_output.split('\n')

    for i, line in enumerate(lines):
        # Skip header lines
        if line.strip() and line[0].isdigit():
            parts = line.split()

            # Ensure timing columns are reformatted with desired precision
            if len(parts) > 3:  # ncalls, tottime, percall, cumtime, percall, filename
                for j in range(1, 5):  # Only modify timing-related columns
                    parts[j] = f'{float(parts[j]):.{precision}f}'
                lines[i] = ' '.join(parts)

    print('\n'.join(lines))


