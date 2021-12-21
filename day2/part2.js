const fs = require('fs')
const prompt = require('prompt-sync')();

const file = fs.readFileSync('input2.txt', 'utf8')

let depth = 0
let horizontal = 0
let aim = 0


data = file.split('\n').map(i => {
    a = i.split(' ')
    a[1] = Number(a[1])
    return a
})

for (let i = 0; i < data.length; i++) {
    item = data[i]
    if (!isNaN(item[1])) {
        if (item[0] === 'forward') {
            horizontal += item[1]
            depth += (aim * item[1])
        }
        if (item[0] === 'up')
            aim -= item[1]
        if (item[0] === 'down')
            aim += item[1]
    }
    console.log(item)
    console.log(aim, depth, horizontal)

    //prompt('contine?')
}

console.log(aim, depth, horizontal)
console.log(depth * horizontal)
