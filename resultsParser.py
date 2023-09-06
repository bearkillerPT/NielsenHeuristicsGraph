def parseHeuristicResults(file_name):
    res = []
    with open(file_name, 'r') as f:
        i = 1
        while line := f.readline():
            if (evaluators_start_location := line.find('(')) != -1: # Line with evaluation
                evaluators_end_location = line.find(')')
                rating_start_location = line.find('-> (') + 3
                rating_end_location = line.find(')', rating_start_location + 1) 
                evaluators = [evaluator.strip() for evaluator in line[evaluators_start_location + 1:evaluators_end_location].strip().split(',')]
                # debug
                # print(i, line[rating_start_location + 1:rating_end_location].strip())
                ratings = [int(rating) for rating in line[rating_start_location + 1:rating_end_location].strip().split(',')]
                res.append((tuple(evaluators), tuple(ratings)))
            i += 1
    return res

if __name__ == "__main__":
    print(parseHeuristicResults("example.txt"))