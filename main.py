from summarizer import NewsSummarizer


def main() -> None:
    """Run the workflow and print the resulting payload."""
    summarizer = NewsSummarizer()
    result = summarizer.run_workflow(article_limit=3)
    print("Workflow output:")
    print(result)


if __name__ == "__main__":
    main()
