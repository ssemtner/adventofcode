const std = @import("std");
const ArrayList = std.ArrayList;

const input = @embedFile("data/day2.txt");
const alloc = std.heap.page_allocator;
const Data = ArrayList(ArrayList(i32));

fn deinit(data: Data) void {
    defer data.deinit();
    for (data.items) |line| {
        line.deinit();
    }
}

fn process(contents: []const u8) !Data {
    var data = ArrayList(ArrayList(i32)).init(alloc);
    var lines = std.mem.tokenizeScalar(u8, contents, '\n');
    while (lines.next()) |line| {
        var row = ArrayList(i32).init(alloc);
        var it = std.mem.tokenizeScalar(u8, line, ' ');
        while (it.next()) |num| {
            try row.append(try std.fmt.parseInt(i32, num, 10));
        }
        try data.append(row);
    }
    return data;
}

fn safe(levels: ArrayList(i32)) bool {
    var last = levels.items[0];
    const inc = levels.items[1] > last;
    for (levels.items[1..]) |level| {
        const diff = @abs(level - last);
        if (diff < 1 or diff >= 4 or (inc and level <= last) or (!inc and level >= last)) {
            return false;
        }
        last = level;
    }
    return true;
}

fn part1(data: Data) !u64 {
    var sum: u64 = 0;
    for (data.items) |row| {
        if (safe(row)) {
            sum += 1;
        }
    }
    return sum;
}

fn part2(data: Data) !u64 {
    var sum: u64 = 0;
    for (data.items) |row| {
        if (safe(row)) {
            sum += 1;
            continue;
        }
        for (0..row.items.len) |i| {
            var changed = ArrayList(i32).init(alloc);
            try changed.appendSlice(row.items[0..i]);
            try changed.appendSlice(row.items[i + 1 ..]);
            if (safe(changed)) {
                sum += 1;
                break;
            }
        }
    }
    return sum;
}

pub fn main() !void {
    const data = try process(input);
    defer deinit(data);
    std.debug.print("Part 1: {d}\n", .{try part1(data)});
    std.debug.print("Part 2: {d}\n", .{try part2(data)});
}

test "Part 1" {
    const testInput =
        \\7 6 4 2 1
        \\1 2 7 8 9
        \\9 7 6 2 1
        \\1 3 2 4 5
        \\8 6 4 4 1
        \\1 3 6 7 9
    ;
    const data = try process(testInput);
    defer deinit(data);
    try std.testing.expectEqual(2, try part1(data));
}

test "Part 2" {
    const testInput =
        \\7 6 4 2 1
        \\1 2 7 8 9
        \\9 7 6 2 1
        \\1 3 2 4 5
        \\8 6 4 4 1
        \\1 3 6 7 9
    ;
    const data = try process(testInput);
    defer deinit(data);
    try std.testing.expectEqual(4, try part2(data));
}
