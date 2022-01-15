import React from 'react';
import axios from 'axios';

const baseURL = "https://jsonplaceholder.typicode.com/posts/1";

export const HomePage = () => {
    const [post, setPost] = React.useState(null);

    React.useEffect(() => {
        axios.get(baseURL).then((response) => {
            setPost(response.data);
        });
    }, []);

    if (!post) return null;


    return(
        <div>
            <h2>Welcome to the home page</h2>
            <p>A well-organized paragraph supports or develops a single controlling idea, which is expressed in a sentence called the topic sentence. A topic sentence has several important functions: it substantiates or supports an essay’s thesis statement; it unifies the content of a paragraph and directs the order of the sentences; and it advises the reader of the subject to be discussed and how the paragraph will discuss it. Readers generally look to the first few sentences in a paragraph to determine the subject and perspective of the paragraph. That’s why it’s often best to put the topic sentence at the very beginning of the paragraph. In some cases, however, it’s more effective to place another sentence before the topic sentence—for example, a sentence linking the current paragraph to the previous one, or one providing background information.</p>


            <h2>This is a test run</h2>
            <p>{post.title}</p>
            <p>{post.body}</p>
        </div>
    );
};
