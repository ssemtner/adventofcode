// Call is_sample from inside a solution to have magic side effects tell you if it's a sample test
// case. It happens so rarely and I didn't want to redo it all with an inner function for tests.

use std::cell::Cell;

thread_local! {
    static IS_SAMPLE: Cell<bool> = const { Cell::new(false) };
}

pub fn is_sample() -> bool {
    IS_SAMPLE.get()
}

pub fn set_sample(val: bool) {
    IS_SAMPLE.set(val);
}
