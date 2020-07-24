def get_tracks(distance):
    v = 0
    t = 0.3
    tracks = []
    current = 0
    mid = distance * 5 / 6

    while current < distance:
        if current < mid:
            a = 2
        else:
            a = -3
        v0 = v
        s = v0 * t + 0.5 * a * (t ** 2)
        current += s
        tracks.append(round(s))
        v = v0 + a * t
    if current > distance:
        tracks.append(distance - current)
    return tracks

print(get_tracks(101))