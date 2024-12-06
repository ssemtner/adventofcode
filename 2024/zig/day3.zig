// run with -Ilib to include regex_wrapper.h

const std = @import("std");
const print = std.debug.print;
const re = @cImport(@cInclude("regex_wrapper.h"));

const input = @embedFile("data/day3.txt");

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    const alloc = gpa.allocator();

    const slice = try alloc.alignedAlloc(u8, re.alignof_regex_t, re.sizeof_regex_t);
    defer alloc.free(slice);
    const regex: [*]re.regex_t = @ptrCast(slice.ptr);

    if (re.regcomp(regex, "mul\\(([0-9]+),([0-9]+)\\)|(do)\\(\\)|(don't)\\(\\)", re.REG_EXTENDED | re.REG_ICASE) != 0) {
        return;
    }

    var matches: [5]re.regmatch_t = undefined;
    var offset: u64 = 0;
    var part1: u64 = 0;
    var part2: u64 = 0;
    var enabled: bool = true;
    while (re.regexec(regex, input[offset..], matches.len, &matches, 0) == 0) {
        if (matches[3].rm_so >= 0) {
            enabled = true;
        } else if (matches[4].rm_so >= 0) {
            enabled = false;
        }
        const a = try match_to_int(matches, 1, offset);
        const b = try match_to_int(matches, 2, offset);
        offset += @intCast(matches[0].rm_eo);
        part1 += a * b;
        if (enabled) {
            part2 += a * b;
        }
    }
    print("Part 1: {d}\n", .{part1});
    print("Part 2: {d}\n", .{part2});
}

fn match_to_int(matches: [5]re.regmatch_t, i: usize, offset: u64) !u64 {
    const m = matches[i];
    if (m.rm_so < 0) {
        return 0;
    }
    const rm_so: u64 = @intCast(m.rm_so);
    const rm_eo: u64 = @intCast(m.rm_eo);
    const start = rm_so + offset;
    const end = rm_eo + offset;
    if (start >= input.len or end >= input.len) {
        return 0;
    }
    const match = input[start..end];
    const num = try std.fmt.parseInt(u64, match, 10);
    return num;
}
