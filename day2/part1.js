const fs = require('fs')

const data = fs.readFileSync('input2.txt', 'utf8')

let d = 0
let h = 0

data.split('\n').map(i => {
    a = i.split(' ')
    a[1] = Number(a[1])
    return a
}).forEach(item => {
    if (isNaN(item)) {
        if (item[0] === 'forward')
            h += item[1]
        if (item[0] === 'up')
            d += item[1]
        if (item[0] === 'down')
            d -= item[1]
    }
})

console.log(d, h)
console.log(d * h)
