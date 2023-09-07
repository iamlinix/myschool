def load() -> (int, int):
    page, index = 0, 0
    try:
        with open('breakpoint', 'r') as f:
            parts = f.readline().split(',')
            page = int(parts[0])
            index = int(parts[1])
    except:
        pass
    return page, index

def store(page: int, index: int):
    try:
        with open('breakpoint', 'w') as f:
            f.write('%d,%d' % (page, index))
            f.flush()
    except:
        pass