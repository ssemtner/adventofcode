const std = @import("std");

const input = @embedFile("data/day1.txt");
const alloc = std.heap.page_allocator;
const Data = std.meta.Tuple(&.{ std.ArrayList(u32), std.ArrayList(u32) });

fn process(contents: []const u8) !Data {
    var a = std.ArrayList(u32).init(alloc);
    var b = std.ArrayList(u32).init(alloc);

    var lines = std.mem.tokenizeScalar(u8, contents, '\n');
    while (lines.next()) |line| {
        if (std.mem.indexOf(u8, line, "   ")) |idx| {
            try a.append(try std.fmt.parseInt(u32, line[0..idx], 10));
            try b.append(try std.fmt.parseInt(u32, line[idx + 3 ..], 10));
        }
    }

    return .{ a, b };
}

fn part1(data: Data) !u64 {
    const a = data[0];
    const b = data[1];
    std.mem.sort(u32, a.items, {}, std.sort.asc(u32));
    std.mem.sort(u32, b.items, {}, std.sort.asc(u32));
    const len = a.items.len;
    var sum: u64 = 0;
    for (0..len) |i| {
        sum += @abs(@as(i64, a.items[i]) - @as(i64, b.items[i]));
    }
    return sum;
}

fn part2(data: Data) !u64 {
    var sum: u32 = 0;

    var map = std.AutoHashMap(u32, u32).init(alloc);
    defer map.deinit();

    for (data[1].items) |x| {
        const res = try map.getOrPut(x);
        if (!res.found_existing) {
            try map.put(x, 1);
        } else {
            try map.put(x, res.value_ptr.* + 1);
        }
    }

    for (data[0].items) |x| {
        if (map.getEntry(x)) |res| {
            sum += x * res.value_ptr.*;
        }
    }

    return @as(u64, sum);
}

pub fn main() !void {
    const data = try process(input);
    defer data[0].deinit();
    defer data[1].deinit();
    std.debug.print("Part 1: {d}\n", .{try part1(data)});
    std.debug.print("Part 2: {d}\n", .{try part2(data)});
}

test "Part 1" {
    const testInput =
        \\3   4
        \\4   3
        \\2   5
        \\1   3
        \\3   9
        \\3   3
    ;
    const data = try process(testInput);
    defer data[0].deinit();
    defer data[1].deinit();
    try std.testing.expectEqual(11, try part1(data));
}

test "Part 2" {
    const testInput =
        \\3   4
        \\4   3
        \\2   5
        \\1   3
        \\3   9
        \\3   3
    ;
    const data = try process(testInput);
    defer data[0].deinit();
    defer data[1].deinit();
    try std.testing.expectEqual(31, try part2(data));
}
