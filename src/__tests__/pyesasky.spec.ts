import { Events } from 'backbone'; // Backbone's Events utility for event-driven behavior
/**
 * Example of [Jest](https://jestjs.io/docs/getting-started) unit tests
 */

describe('pyesasky', () => {
  it('should be tested', () => {
    expect(1 + 1).toEqual(2);
  });
});




test('handle_custom_message is called on msg:custom event', () => {
    const mockContext = {
        handle_custom_message: jest.fn(), // Spy on the handler to check if it's called
    };

    const mockModel = Object.assign({}, Events); // Use Backbone's Events to simulate a model

    // Bind the event
    mockModel.on('msg:custom', mockContext.handle_custom_message, mockContext);

    // Trigger the event
    mockModel.trigger('msg:custom');

    // Verify that the handler was called
    expect(mockContext.handle_custom_message).toHaveBeenCalled();
    expect(mockContext.handle_custom_message.mock.instances[0]).toBe(mockContext); // Ensure correct context
});