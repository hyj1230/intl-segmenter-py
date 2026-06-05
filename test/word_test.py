fn test_words() {
    use crate::testdata::TEST_WORD;

    // Unicode's official tests don't really test longer chains of flag emoji
    // TODO This could be improved with more tests like flag emoji with interspersed Extend chars and ZWJ
    const EXTRA_TESTS: &[(&str, &[&str])] = &[
        (
            "🇦🇫🇦🇽🇦🇱🇩🇿🇦🇸🇦🇩🇦🇴",
            &["🇦🇫", "🇦🇽", "🇦🇱", "🇩🇿", "🇦🇸", "🇦🇩", "🇦🇴"],
        ),
        ("🇦🇫🇦🇽🇦🇱🇩🇿🇦🇸🇦🇩🇦", &["🇦🇫", "🇦🇽", "🇦🇱", "🇩🇿", "🇦🇸", "🇦🇩", "🇦"]),
        (
            "🇦a🇫🇦🇽a🇦🇱🇩🇿🇦🇸🇦🇩🇦",
            &["🇦", "a", "🇫🇦", "🇽", "a", "🇦🇱", "🇩🇿", "🇦🇸", "🇦🇩", "🇦"],
        ),
        (
            "\u{1f468}\u{200d}\u{1f468}\u{200d}\u{1f466}",
            &["\u{1f468}\u{200d}\u{1f468}\u{200d}\u{1f466}"],
        ),
        ("😌👎🏼", &["😌", "👎🏼"]),
        // perhaps wrong, spaces should not be included?
        ("hello world", &["hello", " ", "world"]),
        ("🇨🇦🇨🇭🇿🇲🇿 hi", &["🇨🇦", "🇨🇭", "🇿🇲", "🇿", " ", "hi"]),
    ];
    for &(s, w) in TEST_WORD.iter().chain(EXTRA_TESTS.iter()) {
        macro_rules! assert_ {
            ($test:expr, $exp:expr, $name:expr) => {
                // collect into vector for better diagnostics in failure case
                let testing = $test.collect::<Vec<_>>();
                let expected = $exp.collect::<Vec<_>>();
                assert_eq!(
                    testing, expected,
                    "{} test for testcase ({:?}, {:?}) failed.",
                    $name, s, w
                )
            };
        }
        // test forward iterator
        assert_!(
            s.split_word_bounds(),
            w.iter().cloned(),
            "Forward word boundaries"
        );

        // test reverse iterator
        assert_!(
            s.split_word_bounds().rev(),
            w.iter().rev().cloned(),
            "Reverse word boundaries"
        );

        // generate offsets from word string lengths
        let mut indices = vec![0];
        for i in w.iter().cloned().map(|s| s.len()).scan(0, |t, n| {
            *t += n;
            Some(*t)
        }) {
            indices.push(i);
        }
        indices.pop();
        let indices = indices;

        // test forward indices iterator
        assert_!(
            s.split_word_bound_indices().map(|(l, _)| l),
            indices.iter().cloned(),
            "Forward word indices"
        );

        // test backward indices iterator
        assert_!(
            s.split_word_bound_indices().rev().map(|(l, _)| l),
            indices.iter().rev().cloned(),
            "Reverse word indices"
        );
    }
}